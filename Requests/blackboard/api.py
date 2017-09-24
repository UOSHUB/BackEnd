from . import root_url as url
from .values import __terms
import requests

# Append Blackboard API path to root URL
url += "learn/api/public/v1/"


# General Blackboard API request with common attributes
def get(link, session, params=None):
    return requests.get(
        # Get data from api url + api sub-url
        url + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).json()


# Get student's basic info (name, major, collage)
def basic_info(session, sid):
    # Request data from API url while passing student id
    student = get("users/userName:" + sid, session, {"fields": "name,job"})
    # Extract and return a dictionary of student info
    return {
        "name": student["name"]["given"],
        "major": student["job"]["department"],
        "collage": student["job"]["company"]
    }


# Get student's current term code
def current_term(session, sid):
    # Get student's courses while passing his id
    date = get("users/userName:" + sid + "/courses", session, {
        # Only return the field "created" and sort by it
        "fields": "created",
        "sort": "created"
        # Select student's latest course creation date
    })["results"][-1]["created"]
    # Extract term code by concatenating year and semester code according to the month
    return date[:4] + (int(date[6]) > 7 and "10" or date[6] < "6" and "20" or "30")


# Returns student's list of courses
def courses(session, term, sid):
    # Store term year and months range start and end
    start, end = __terms[term[4:]]["range"]
    year = term[:4]
    return [
        # Return an array of courses ids
        course["courseId"][1:-2]
        # Get and loop through student's courses while passing his id
        for course in get("users/userName:" + sid + "/courses", session, {
            # Only return the field "created" and sort by it
            "fields": "created,courseId,courseRoleId"
            # Select student's latest course creation date
        })["results"][-10:]
        # Only return courses from requested year
        if course["created"][:4] == year and
        # And in the range of months of requested term
        start >= int(course["created"][5:7]) >= end and
        # And which role is 'Student'
        course["courseRoleId"] == "Student"
    ]
