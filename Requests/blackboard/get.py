import requests

# Root url of Blackboard
root_url = "https://elearning.sharjah.ac.ae/webapps/"
# General Blackboard items id format
__id = "_{}_1"


# Logs in Blackboard and returns the session
def __login(sid, pin):
    # Post HTTP request and store its response
    response = requests.post(
        # Post data to login url
        root_url + "login/",
        # Send student id and password
        data={"user_id": sid, "password": pin}
    )
    # For some reason, response is encoded in 'ISO-8859-1'
    # only when login succeeds, otherwise
    if response.encoding != 'ISO-8859-1':
        # Raise an error to indicate login failure
        raise ConnectionError("Wrong Credentials!")
    # If login succeeded, send back session cookies
    return response.cookies.get_dict()


# General Blackboard data request with common attributes
def data(link, session, params=None):
    return requests.get(
        # Get data from root url + sub url
        root_url + link,
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
        "modId": __id.format({
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
        "tabId": __id.format(1),
    })


# Gets course's specific menu (on the left side)
def course_menu(session, course_id):
    # Get data from course menu url
    return data("blackboard/content/courseMenu.jsp", session, {
        # Specify requested course id
        "course_id": __id.format(course_id)
    })


# Gets page of announcements for all courses or for one course by id
def announcements(session, course_id=None):
    # Get data from announcements url
    return data("blackboard/execute/announcement", session, {
        # By default get all course announcements, if course id is sent then only get the sent one
        "method": "search", "searchSelect": course_id or "announcement.coursesonly.label"
    })


# Gets student's Blackboard profile image page
def profile_image(session):
    # Get data from Blackboard flyout menu url
    return data("portal/execute/globalNavFlyout", session, {
        # Required parameter
        "cmd": "view"
    })


# Get direct list of courses
def courses(session):
    # Get data from top right navigation menu
    return data("blackboard/execute/globalCourseNavMenuSection", session, {
        # Required parameter
        "cmd": "view"
    }).text


# Gets the (not used) tasks page
def __tasks(session):
    # Get data from tasks management page
    return data("blackboard/execute/taskEditList", session)
