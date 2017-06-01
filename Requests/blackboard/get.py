import requests

root_url = "https://elearning.sharjah.ac.ae/webapps/"

__QUERIES = {
    "Announcements": 1,
    "Courses": 4,
    "Organizations": 5,
    "Tasks": 7,
    "Notes": 12,
    "Grades": 20,
    "Collages": 28,
    "Surveys": 257
}


def __login(sid, pin):
    return requests.post(
        root_url + "login/",
        data={"user_id": sid, "password": pin}
    ).cookies


def list_of(session, query):
    return requests.post(
        root_url + "portal/execute/tabs/tabAction",
        cookies=session,
        data={
            "action": "refreshAjaxModule",
            "modId": "_{}_1".format(__QUERIES[query]),
            "tabId": "_1_1",
        }
    ).text


def course_menu(session, course_id):
    return requests.get(
        root_url + "blackboard/content/courseMenu.jsp",
        cookies=session,
        params={"course_id": course_id}
    ).text


def announcements(session, course_id=None):
    return requests.get(
        root_url + "blackboard/execute/announcement",
        cookies=session,
        params={
            "method": "search",
            "searchSelect": course_id or "announcement.coursesonly.label"
        }
    ).text


def profile_image(session):
    return requests.get(
        root_url + "portal/execute/globalNavFlyout",
        cookies=session,
        params={"cmd": "view"}
    ).text


def courses(session):
    return requests.get(
        root_url + "blackboard/execute/globalCourseNavMenuSection",
        cookies=session,
        params={"cmd": "view"}
    ).text


def __tasks(session):
    return requests.get(
        root_url + "blackboard/execute/taskEditList",
        cookies=session
    ).text
