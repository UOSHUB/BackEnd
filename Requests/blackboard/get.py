from . import root_url as url, __id
from .values import __lists
import requests, time

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


# Gets updates and announcements in a JSON object
def updates(session):
    # Store Blackboard stream url
    stream_url = url + "streamViewer/streamViewer"
    # Request updates from Blackboard stream and store returned cookies
    stream_cookies = requests.get(stream_url, cookies=session, params={
        "cmd": "view",
        "streamName": "alerts"
    }).cookies
    # Wait a bit until updates are ready
    time.sleep(.05)
    # Loop until they are ready or something happens
    for _ in range(8):
        # Request updates using previous cookies, and convert response to JSON
        response = requests.post(stream_url, cookies=stream_cookies, data={
            # Pass required parameters
            "cmd": "loadStream",
            "streamName": "alerts",
            "forOverview": "false",
            "providers": "{}",
        }).json()
        # Return response if it contains requested data
        if response["sv_streamEntries"]:
            return response


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
        "modId": __id(__lists[query]),
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
