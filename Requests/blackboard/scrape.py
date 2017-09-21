# Import two html processing functions as hidden variables
from lxml.html import fromstring as __parse_html, tostring as __get_html
from .values import __types, __events


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
            "courseId": details["courseId"],
            "contentId": details["sourceId"],
            # Store title, course and time
            "title": item["title"],
            "course": courses_names[details["courseId"]],
            "time": update["se_timestamp"],
            # Get meaningful equivalent of event from stored values
            "event": __types[event[0]] + (
                # Add event type as long as it's not an announcement
                " " + __events[event[1].split('_')[-1]] if event[0] != "AN" else ""
            )
        })
    return updates_array


# Scrapes courses ids from list_of("Courses") and courses()
def courses(response, from_list_of=False):
    # Determine scraped attribute and location of course id
    # depending on whether the sent data is from list_of() or courses() functions
    attr, start, end = ("href", 54, -7) if from_list_of else ("onclick", 87, -24)
    # Return dictionary of courses blackboard ids mapped to courses myUDC ids
    return {link.text[:7]: link.attrib[attr][start:end] for link in __parse_html(response).xpath("//a")}


# Scrapes announcements' useful data
def announcements(response):
    # Parse page's html and store it
    page = __parse_html(response)
    # Store course ids dictionary
    ids = {
        # Store values in {course name: course id} pairs
        course.text[1:]: course.get("value")
        # Loop through student's available courses
        for course in page.findall(".//select[@id='searchSelectId']/option")[3:]
    }
    # Array to store announcements dictionaries
    messages = []
    # Loop through announcements
    for item in page.findall(".//ul[@id='announcementList']/li"):
        # Add announcement to the array
        messages.append({
            # Clear announcement title from white spaces and store it
            "title": item.find("h3[@class='item']").text.strip(),
            # Store raw announcement body in html format after encoding in utf-8
            "body": __get_html(item.find(".//div[@class='vtbegenerated']")).decode(),
            # Store announcement date from first paragraph in ".details" tag
            "date": item.find("div[@class='details']/p/span").text[11:],
            # Store announcement's associated course id
            "id": ids[item.find("div[@class='announcementInfo']/p[2]").text_content()[11:]],
        })
    return messages
