from lxml.etree import fromstring as __parse_xml
from .get import url, data
from . import __id
import requests

# Append Blackboard Mobile path to website URL
sub_url = "Bb-mobile-bb_bb60/"
url += sub_url


# Logs in Blackboard Mobile and returns the session
def login(sid, pin):
    # Post HTTP request and store its response
    response = requests.post(
        # Post data to login url
        url + "sslUserLogin",
        # Send student id and password
        data={"username": sid, "password": pin}
    )
    # If response status is not "OK"
    if "OK" not in response.text:
        # Raise an error to indicate login failure
        raise ConnectionError("Wrong Credentials!")
    # If login succeeded, send back session cookies
    return response.cookies.get_dict()


# Returns student's list of courses
def courses(session, term):
    term = {"10": "FALL", "30": "SUM", "20": "SPR"}[term[4:]] + term[:4]
    # Get data from enrollments data url while specifying that requested type is "course"
    return [
        course.get("bbid")[1:-2]
        for course in __parse_xml(data(
            sub_url + "enrollments", session, {"course_type": "COURSE"}
        ).encode()).find(".//courses")
        if term in course.get("courseid") and course.get("roleIdentifier") == "S"
    ]


# Returns a specific course's data by its id
def course_data(session, course_id, section):
    # Get data from course data url
    return data(sub_url + "courseData", session, {
        # Send course id
        "course_id": __id(course_id),
        # Currently known possible values are
        # "ANNOUNCEMENTS" and "GRADES"
        "course_section": section,
        # This flag reduces HTML junk
        "rich_content_level": "RICH"
    })
