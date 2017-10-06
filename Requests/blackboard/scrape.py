from .values import __types, __events, __terms
from lxml.etree import fromstring as __parse_xml
import re

# Regex for selecting English letters and cleaning numbers
__english = re.compile("[^\w /&.]", re.ASCII)
__clean_end = re.compile("[0-9]+$")
# Regex for selecting attachment's id and its content id
__content_id = re.compile("content_id=_([0-9]+)_1")
__file_id = re.compile("xid-([0-9]+)_1")


# Cleans course name
def __clean(name):
    # From non English letters and from section numbers at the end
    return __clean_end.sub("", __english.sub("", name).strip()).strip()


# Scrapes useful data from updates JSON object
def updates(response):
    # Array to store updates
    updates_array = []
    # Dictionary of courses names for later use
    courses_names = {
        # Loop through courses and store their name and id
        course["id"]: course["name"].split("-")[0]
        for course in response["sv_extras"]["sx_courses"]
    }
    # Loop through updates
    for update in response["sv_streamEntries"]:
        # Store repeatedly used references of the object
        event = update["extraAttribs"]["event_type"].split(":")
        item = update["itemSpecificData"]
        details = item["notificationDetails"]
        # Append the update as a dictionary to updates array
        updates_array.append({
            # Store all ids related to the update
            "updateId": details["actorId"],
            "courseId": int(details["courseId"][1:-2]),
            "contentId": int(details["sourceId"][1:-2]),
            # Store title, course and time
            "title": item["title"],
            "course": courses_names[details["courseId"]],
            "time": update["se_timestamp"],
            # Get meaningful equivalent of event from stored values
            "event": __types[event[0]] + (
                # Add event type as long as it's not an announcement
                " " + __events.get(event[1].split("_")[-1], "") if event[0] != "AN" else ""
            )
        })
    return updates_array


# Scrapes student's list of all courses categorized by term
def courses_list(response, url=lambda x: x):
    terms = {}
    # Loop through courses registered in Blackboard
    for course in __parse_xml(response).findall(".//course[@roleIdentifier='S']"):
        # Extract course key, crn and term from course id
        key, crn, term = course.get("courseid").split("_")
        # Make sure that term id is of the following format "FALL2017"
        term = term.split("-")[0]
        # Split term id to year and term short name
        year, short = term[-4:], term[:-4]
        # Get term full name of the following format "Fall 2017-2018"
        term = "{} {}-{}".format(__terms[short]["name"], year, int(year) + 1)
        # If term hasn't been added yet
        if term not in terms:
            # Initialize it with an empty dictionary
            terms[term] = {}
        # Add course to the correspondent term
        terms[term][__clean(course.get("name"))] = {
            # Content links to Blackboard's documents and deadlines
            "Content": url(course.get("bbid")[1:-2]),
            # Details links to MyUDC's course details
            "Details": url("{}/{}/{}".format(key, crn, year + __terms[short]["code"]))
        }
    return terms


# Scrapes student's list of courses by term
def courses_by_term(response, term):
    courses = {}
    # Get Blackboard term name in "FALL2017" format from term code
    term = __terms[term[4:]]["name"] + term[:4]
    # Loop through list of courses in parsed xml
    for course in __parse_xml(response).find(".//courses"):
        # Store course's Blackboard code
        code = course.get("courseid")
        # Only add courses in the requested term and that are with "Student" role
        if term in code and course.get("roleIdentifier") == "S":
            # Extract course key and crn from code
            key, crn = code.split("_")[:2]
            # Add course data after cleaning
            courses[key] = {
                "title": __clean(course.get("name")),
                # Store course's Blackboard id
                "bb": course.get("bbid")[1:-2],
                "crn": crn
            }
    return courses


# Scrapes student's specific course data
def course_data(response, data_type=None):
    # Store parsed course and returned object structure
    course = __parse_xml(response)
    data = {"deadlines": [], "documents": []}
    # If requested data type isn't "documents"
    if data_type != "documents":
        # Scrape deadlines and add them to data
        data["deadlines"] = [
            {  # Store deadline's title, due date and content id
                "title": deadline.get("name"),
                "dueDate": deadline.get("dueDate"),
                "contentId": int(deadline.get("contentid")[1:-2])
            }  # Loop through all course items which have a due date
            for deadline in course.findall(".//*[@dueDate]")
        ]
        # If requested data type is "deadlines"
        if data_type == "deadlines":
            # Only return the deadlines
            return data["deadlines"]
    # If requested data type isn't "deadlines"
    if data_type != "deadlines":
        # Loop through all course documents
        for document in course.findall(".//attachment"):
            # Store document's url for later use
            url = document.get("url")
            # Add document dictionary to data
            data["documents"].append({
                # Store document's title, upload date
                "title": document.getparent().getparent().get("name"),
                "file": document.get("name"),
                "uploadDate": document.get("modifiedDate"),
                # From document's URL, get its id and content id using Regex
                "contentId": int(__content_id.search(url).group(1)),
                "fileId": int(__file_id.search(url).group(1))
            })
        # If requested data type is "documents"
        if data_type == "documents":
            # Only return the documents
            return data["documents"]
    # Return everything if data type isn't specified or invalid
    return data
