from . import root_url as url, __id
import requests

# Append Blackboard website path to root URL
url += "webapps/"


# Logs in Blackboard and returns the session
def __login(sid, pin):
    # Post HTTP request and store its response
    response = requests.post(
        # Post data to login url
        url + "login/",
        # Send student id and password
        data={"user_id": sid, "password": pin}
    )
    # For some reason, response is encoded in "ISO-8859-1"
    # only when login succeeds, otherwise
    if response.encoding != "ISO-8859-1":
        # Raise an error to indicate login failure
        raise ConnectionError("Wrong Credentials!")
    # If login succeeded, send back session cookies
    return response.cookies.get_dict()


# General Blackboard request to "webapps/" with common attributes
def data(link, session, params=None):
    return requests.get(
        # Get data from website url + sub-url
        url + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).text


# Gets list of one of the options listed below through AJAX
def list_of(session, query):
    # Get data from AJAX requests url
    return data("portal/execute/tabs/tabAction", session, {
        # Get list through AJAX
        "action": "refreshAjaxModule",
        # Get list of one of these options
        "modId": __id({
            # Available lists
            "Announcements": 1,
            "Courses": 4,
            "Organizations": 5,
            "Tasks": 7,
            "Notes": 12,
            "Grades": 20,
            "Collages": 28,
            "Surveys": 257
            # Select one of them
        }[query]),
        # Required parameter
        "tabId": __id(1),
    })


# Gets page of announcements for all courses or for one course by id
def announcements(session, course_id=None):
    # Get data from announcements url
    return data("blackboard/execute/announcement", session, {
        # By default get all course announcements, if course id is sent then only get the sent one
        "method": "search", "searchSelect": course_id or "announcement.coursesonly.label"
    })


# Get direct list of courses
def courses(session):
    # Get data from top right navigation menu
    return data("blackboard/execute/globalCourseNavMenuSection", session, {
        # Required parameter
        "cmd": "view"
    }).text
