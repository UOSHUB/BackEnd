import requests

# Root url of UOS Blackboard
root_url = "https://elearning.sharjah.ac.ae/"
# General Blackboard items id format
__id = "_{}_1"


# Logs in Blackboard and returns the session
def __login(sid, pin):
    # Post HTTP request and store its response
    response = requests.post(
        # Post data to login url
        root_url + 'webapps/login/',
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


# General Blackboard API request with common attributes
def api(link, session, params=None):
    return requests.get(
        # Get data from root url + api url
        root_url + 'learn/api/public/v1/' + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).json()


# Get student's basic info (name, major, collage)
def basic_info(session, sid):
    # Request data from API url while passing student id
    student = api('users/userName:' + sid, session, {'fields': 'name,job'})
    # Extract and return a dictionary of student info
    return {
        'name': student['name']['given'],
        'major': student['job']['department'],
        'collage': student['job']['company']
    }


# General Blackboard request to 'webapps/' with common attributes
def web(link, session, params=None):
    return requests.get(
        # Get data from root url + web url
        root_url + 'webapps/' + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).text


# Gets list of one of the options listed below through AJAX
def list_of(session, query):
    # Get data from AJAX requests url
    return web("portal/execute/tabs/tabAction", session, {
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


# Gets page of announcements for all courses or for one course by id
def announcements(session, course_id=None):
    # Get data from announcements url
    return web("blackboard/execute/announcement", session, {
        # By default get all course announcements, if course id is sent then only get the sent one
        "method": "search", "searchSelect": course_id or "announcement.coursesonly.label"
    })


# Get direct list of courses
def courses(session):
    # Get data from top right navigation menu
    return web("blackboard/execute/globalCourseNavMenuSection", session, {
        # Required parameter
        "cmd": "view"
    }).text
