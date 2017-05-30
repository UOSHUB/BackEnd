import requests

root_url = "https://elearning.sharjah.ac.ae/webapps/"


def __login(sid, pin):
    return requests.post(
        root_url + "login/",
        data={"user_id": sid, "password": pin}
    ).cookies


def courses(session, survey=False):
    return requests.post(
        root_url + "portal/execute/tabs/tabAction",
        cookies=session,
        data={
            "action": "refreshAjaxModule",
            "modId": ["_27_1", "_257_1"][survey],
            "tabId": "_1_1",
        }
    ).text


def announcements(session):
    return requests.get(
        root_url + "blackboard/execute/announcement",
        cookies=session,
        params={
            "method": "search",
            # Choose Courses & Organizations
            "viewChoice": 2
        }
    ).text
