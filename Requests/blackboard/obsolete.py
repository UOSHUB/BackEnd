from .get import data
from . import __id


# Gets course's specific menu (on the left side)
def course_menu(session, course_id):
    # Get data from course menu url
    return data("blackboard/content/courseMenu.jsp", session, {
        # Specify requested course id
        "course_id": __id(course_id)
    })


# Gets the tasks page
def tasks(session):
    # Get data from tasks management page
    return data("blackboard/execute/taskEditList", session)


# Scrapes list of courses from survey panel
def survey_courses(response):
    # Using Regex and Json
    import re, json
    # Search for the Json object that contains the course list and parse it
    return json.loads(re.search("json_ecb = ({.*?});", response).group(1))
