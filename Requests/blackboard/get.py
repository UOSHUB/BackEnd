from .general import mobile as __mobile, api as __api, __id, __documents
from .values import __stream_url
import requests, time


# Gets updates and announcements in a JSON object
def updates(session, counter=0):
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
            # Check if updates isn't a Blackboard announcement
            update["providerId"] != "bb-announcement"
            # Loop through updates
            for update in data
            # Return response if it contains requested data
        ): return data
    # If loop finishes with no data, try again or return an empty array
    return updates(session, counter+1) if counter < 3 else []


# Get student's basic info (name, major, college)
def basic_info(session, sid):
    # Request data from API url while passing student id
    student = __api("users/userName:" + sid, session, {"fields": "name,job"})
    # Split last two pieces of last name and store them
    last_name = student["name"]["family"].rsplit(" ", 2)[-2:]
    # If last name has a two characters prefix (e.g. 'Al', 'El', 'Ba')
    if len(last_name) == 2 and len(last_name[0]) == 2:
        # Join the prefix with last name
        last_name[1] = " ".join(last_name)

    # Extract and return a dictionary of student info
    return {
        "lastName": last_name[-1],
        "firstName": student["name"]["given"],
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
def course_grades(session, sid, course_id):
    # Construct course root URL
    course_url = f"courses/{__id(course_id)}/gradebook/"
    # Request course scores from Blackboard API
    scores = __api(
        # Specify current student id
        course_url + "users/userName:" + sid,
        # Send session snd required fields
        session, {"fields": "score,status,columnId"}
    )["results"]
    # If any of the course scores is graded
    if any(score.get("status") == "Graded" for score in scores):
        # Return the scores alongside with their column names
        return scores, __api(
            # Request course grades columns schema
            course_url + "columns", session,
            # Specify required fields
            {"fields": "name,id,score.possible,grading.due"}
        )["results"]


# Download a course's document
def course_document(session, content_id, xid):
    document = requests.get(
        # Get document by content id and xid
        __documents.format(content_id, xid),
        # Send login session
        cookies=session,
    )
    # Return document in form ({content, type}, name)
    return {
        "content": document.content,
        "content_type": document.headers.get("Content-Type")
        # Extract document file name from URL
    }, document.url.rsplit("/", 1)[1]
