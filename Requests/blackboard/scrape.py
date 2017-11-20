from Requests import clean_course_name as __clean
from lxml.etree import fromstring as __parse_xml
from .values import __types, __events, __terms, __root_url_no_slash, __timestamp
from math import ceil


# Scrapes useful data from updates JSON object
def updates(raw_updates, courses):
    # Dictionary to store updates data
    data = []
    # Loop through updates
    for update in raw_updates:
        # Keep a reference of used object indexes
        item = update["itemSpecificData"]
        details = item["notificationDetails"]
        # Extract Blackboard id and store its equivalent MyUDC id
        course = courses.get(details["courseId"][1:-2])
        # Skip non-student courses
        if not course: continue
        # Store update's event parts
        event = update["extraAttribs"]["event_type"].split(":")
        # Append the update as a dictionary to data
        data.append({
            # Store title, time, dismiss id & course key
            "course": course,
            "title": item["title"],
            "dismiss": details["actorId"],
            "time": __timestamp(update["se_timestamp"] / 1000).strftime("%Y-%m-%dT%H:%M:%S") + "+0400",
            # Get meaningful equivalent of event from stored values
            "event": __types[event[0]] + (
                # Add event type as long as it's not an announcement
                " " + __events.get(event[1].split("_")[-1], "") if event[0] != "AN" else ""
            )
        })
    return data


# Scrapes all courses' ids dictionary
def courses_dictionary(response):
    return {
        # Store courses ids in {Blackboard id: MyUDC id} pairs
        course.get("bbid")[1:-2]: course.get("courseid").split("_", 1)[0]
        # Loop through all courses in Blackboard in which the user is a student
        for course in __parse_xml(response).findall(".//course[@roleIdentifier='S']")
    }


# Scrapes student's list of all terms available in Blackboard
def terms_list(response):
    terms = {}
    # Loop through courses registered in Blackboard
    for course in __parse_xml(response).findall(".//course[@roleIdentifier='S']"):
        # Extract term's from course id in "FALL2017" format
        term = course.get("courseid").rsplit("_", 1)[-1].split("-")[0]
        # Split term id to year and term semester
        year, semester = term[-4:], __terms[term[:-4]]
        # Store term in terms in {"Fall 2017-2018": "201710"} pairs
        terms["{} {}-{}".format(semester["name"], year, int(year) + 1)] = year + semester["code"]
    return terms


# Scrapes student's list of all courses categorized by term
def courses_list(response, url=lambda x: x):
    terms = {}
    # Loop through courses registered in Blackboard
    for course in __parse_xml(response).findall(".//course[@roleIdentifier='S']"):
        # Extract course key, crn and term from course id
        key, crn, term = course.get("courseid").split("_")
        # Make sure that term id is of the following format "FALL2017"
        term = term.split("-")[0]
        # Split term id to year and semester
        year, semester = term[-4:], __terms[term[:-4]]
        # Get term full name of the following format "Fall 2017-2018"
        term = "{} {}-{}".format(semester["name"], year, int(year) + 1)
        # If term hasn't been added yet
        if term not in terms:
            # Initialize it with an empty dictionary
            terms[term] = {}
        # Add course to the correspondent term
        terms[term][__clean(course.get("name"))] = {
            # Content links to Blackboard's documents and deadlines
            "Content": url(key + "/" + course.get("bbid")[1:-2]),
            # Details links to MyUDC's course details
            "Details": url("{}/{}/{}".format(key, crn, year + semester["code"]))
        }
    return terms


# Scrapes student's list of courses' ids by term
def courses_by_term(response, term):
    courses = {}
    # Get Blackboard term name in "FALL2017" format from term code
    term = __terms[term[4:]]["name"] + term[:4]
    # Loop through list of courses in parsed xml
    for course in __parse_xml(response).find("courses"):
        # Store course's Blackboard code
        key, crn, full_term = course.get("courseid").split("_")
        # Only add courses in the requested term and in which the user is a student
        if full_term.startswith(term) and course.get("roleIdentifier") == "S":
            # Add course ids in {MyUDC id: Blackboard id} pairs
            courses[key] = {
                # Store course's Blackboard id
                "courseId": course.get("bbid")[1:-2],
                "crn": crn
            }
    return courses


# Scrapes student's specific course data
def course_data(response, key, data_type=None):
    # Store parsed course and returned object structure
    course = __parse_xml(response)
    data = {"deadlines": [], "documents": []}
    # If requested data type isn't "documents"
    if data_type != "documents":
        # Scrape deadlines and add them to data
        data["deadlines"] = [
            {   # Store deadline's title, due date & course key
                "course": key,
                "title": deadline.get("name"),
                "dueDate": deadline.get("dueDate"),
                "time": deadline.get("createdDate")
            }   # Loop through all course items which have a due date
            for deadline in course.findall(".//*[@dueDate]")
        ]
        # If requested data type is "deadlines"
        if data_type == "deadlines":
            # Only return the deadlines
            return data["deadlines"]
    # If requested data type isn't "deadlines"
    if data_type != "deadlines":
        # Scrape documents and add them to data
        data["documents"] = [
            {   # Store document's title, upload date & course key
                "course": key,
                "title": document.getparent().getparent().get("name"),
                "file": document.get("name"),
                "time": document.get("modifiedDate"),
                # From document's URL, get its id and content id using Regex
                "url": __root_url_no_slash + document.get("url")
            }   # Loop through all course documents
            for document in course.findall(".//attachment")
        ]
        # If requested data type is "documents"
        if data_type == "documents":
            # Only return the documents
            return data["documents"]
    # Return everything if data type isn't specified or invalid
    return data


# Scrapes student's specific course grades
def course_grades(response, key):
    grades = []
    # Loop through grades in available in course
    for grade in __parse_xml(response).find("grades"):
        # Store last modified time
        time = grade.get("lastInstructorActivity")
        # If it's a graded items
        if time:
            # Add grade dictionary to grades
            grades.append({
                # Add item's title, grade & course key
                "course": key,
                "title": grade.get("name"),
                "grade": ceil(float(grade.get("grade"))),
                # Add total grade and uploaded time
                "outOf": ceil(float(grade.get("pointspossible"))),
                "time": time
            })
    return grades
