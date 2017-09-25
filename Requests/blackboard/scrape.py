from .values import __types, __events, __terms
from lxml.etree import fromstring as __parse_xml


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
                " " + __events.get(event[1].split("_")[-1], "") if event[0] != "AN" else ""
            )
        })
    return updates_array


# Scrapes student's list of courses
def courses_list(response, term):
    # Get Blackboard term name in "FALL2017" format from term code
    term = __terms[term[4:]]["name"] + term[:4]
    return [
        # Return an array of Blackboard course ids
        course.get("bbid")[1:-2]
        # Loop through list of courses in parsed xml
        for course in __parse_xml(response).find(".//courses")
        # Only return courses from the requested term and that are with "Student" role
        if term in course.get("courseid") and course.get("roleIdentifier") == "S"
    ]
