from .get import url
from . import __id
import requests

# Append Blackboard Mobile path to website URL
url += "Bb-mobile-bb_bb60/"


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
def courses(session):
    return requests.get(
        # Get data from enrollments data url
        url + "enrollments",
        # Send login session
        cookies=session,
        # Specify that requested type is course
        params={"course_type": "COURSE"}
    ).text


# Returns a specific course's data by its id
def course_data(session, course_id, section):
    return requests.get(
        # Get data from course data url
        url + "courseData",
        # Send login session
        cookies=session,
        params={
            # Send course id
            "course_id": __id(course_id),
            # Currently known possible values are
            # "ANNOUNCEMENTS" and "GRADES"
            "course_section": section,
            # This flag reduces HTML junk
            "rich_content_level": "RICH"
        }
    ).text
