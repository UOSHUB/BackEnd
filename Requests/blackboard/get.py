from .general import root_url, mobile as __mobile, api as __api
import requests, time


# Gets updates and announcements in a JSON object
def updates(session):
    # Store Blackboard stream url
    stream_url = root_url + "webapps/streamViewer/streamViewer"
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
    # TODO: if loop finishes without response, get updates from mobile API


# Get student's basic info (name, major, collage)
def basic_info(session, sid):
    # Request data from API url while passing student id
    student = __api("users/userName:" + sid, session, {"fields": "name,job"})
    # Extract and return a dictionary of student info
    return {
        "name": student["name"]["given"],
        "major": student["job"]["department"],
        "collage": student["job"]["company"]
    }


# Gets student's list of courses
def courses_list(session):
    return __mobile(
        # Get courses from enrollments data url
        "enrollments", session,
        # Specify requested type as "course"
        {"course_type": "COURSE"}
    )
