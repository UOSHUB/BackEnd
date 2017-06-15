import requests

# Root url of Blackboard
root_url = "https://elearning.sharjah.ac.ae/webapps/"
# General Blackboard items id format
__id = "_{}_1"


# Logs in Blackboard and returns the session
def __login(sid, pin):
    return requests.post(
        # Post data to login url
        root_url + "login/",
        # Send student id and password
        data={"user_id": sid, "password": pin}
    ).cookies


# Gets list of one of the options listed below through AJAX
def list_of(session, query):
    return requests.get(
        # Get data from AJAX requests url
        root_url + "portal/execute/tabs/tabAction",
        # Send login session
        cookies=session,
        # Send required data
        params={
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
        }
    ).url


# Gets course's specific menu (on the left side)
def course_menu(session, course_id):
    return requests.get(
        # Get data from course menu url
        root_url + "blackboard/content/courseMenu.jsp",
        # Send login session
        cookies=session,
        # Specify requested course id
        params={"course_id": __id.format(course_id)}
    ).text


# Gets page of announcements for all courses or for one course by id
def announcements(session, course_id=None):
    return requests.get(
        # Get data from announcements url
        root_url + "blackboard/execute/announcement",
        # Send login session
        cookies=session,
        # By default get all course announcements, if course id is sent then only get the sent one
        params={"method": "search", "searchSelect": course_id or "announcement.coursesonly.label"}
    ).url


# Gets student's Blackboard profile image page
def profile_image(session):
    return requests.get(
        # Get data from Blackboard flyout menu url
        root_url + "portal/execute/globalNavFlyout",
        # Send login session
        cookies=session,
        # Required parameter
        params={"cmd": "view"}
    ).text


# Get direct list of courses
def courses(session):
    return requests.get(
        # Get data from top right navigation menu
        root_url + "blackboard/execute/globalCourseNavMenuSection",
        # Send login session
        cookies=session,
        # Required parameter
        params={"cmd": "view"}
    ).text


# Gets the (not used) tasks page
def __tasks(session):
    return requests.get(
        # Get data from tasks management page
        root_url + "blackboard/execute/taskEditList",
        # Send login session
        cookies=session
    ).text
