from .general import mobile as __mobile, api as __api, __id
from .values import __stream_url
import requests, time


# Gets updates and announcements in a JSON object
def updates(session):
    # Request updates from Blackboard stream and store returned cookies
    stream_cookies = requests.get(__stream_url, cookies=session, params={
        "cmd": "view",
        "streamName": "alerts"
    }).cookies
    # Wait a bit until updates are ready
    time.sleep(.05)
    # Loop until they are ready or something happens
    for _ in range(8):
        # Request updates using previous cookies, and convert response to JSON
        response = requests.post(__stream_url, cookies=stream_cookies, data={
            # Pass required parameters
            "cmd": "loadStream",
            "streamName": "alerts",
            "forOverview": "false",
            "providers": "{}",
        }).json()
        # Get & store updates from response
        data = response.get("sv_streamEntries")
        # If any of the updates is a course update
        if data and any(
            # Check if updates isn't a Blackboard assignment
            update["providerId"] != "bb-announcement"
            # Loop through updates
            for update in data
            # Return response if it contains requested data
        ): return data
    # If loop finishes with no data, return an empty array
    return []
    # TODO: if loop finishes without response, get updates from mobile API


# Get student's basic info (name, major, college)
def basic_info(session, sid):
    # Request data from API url while passing student id
    student = __api("users/userName:" + sid, session, {"fields": "name,job"})
    # Extract and return a dictionary of student info
    return {
        "firstName": student["name"]["given"],
        "lastName": student["name"]["family"].rsplit(" ", 1)[-1],
        "major": student["job"]["department"],
        "college": student["job"]["company"],
        "studentId": sid
    }


# Gets student's list of courses
def courses_list(session):
    # Request form Blackboard Mobile
    return __mobile(
        # Get courses from enrollments data url
        "enrollments", session,
        # Specify requested type as "course"
        {"course_type": "COURSE"}
    )


# Gets student's specific course data
def course_data(session, course_id):
    # Request form Blackboard Mobile
    return __mobile(
        # Get data from course map url
        "courseMap", session,
        # Specify requested course id
        {"course_id": __id(course_id)}
    )


# Gets student's specific course grades
def course_grades(session, course_id):
    # Request form Blackboard Mobile
    return __mobile(
        # Get data from course data url
        "courseData", session, {
            # Specify section as "grades"
            "course_section": "GRADES",
            # Specify requested course id
            "course_id": __id(course_id)
        }
    )
