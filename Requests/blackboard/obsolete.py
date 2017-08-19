from .get import data, __id


# Gets course's specific menu (on the left side)
def course_menu(session, course_id):
    # Get data from course menu url
    return data("blackboard/content/courseMenu.jsp", session, {
        # Specify requested course id
        "course_id": __id.format(course_id)
    })


# Gets the tasks page
def tasks(session):
    # Get data from tasks management page
    return data("blackboard/execute/taskEditList", session)


# Gets student's Blackboard profile image page (useless in latest update)
def profile_image(session):
    # Get data from Blackboard flyout menu url
    return data("portal/execute/globalNavFlyout", session, {
        # Required parameter
        "cmd": "view"
    })


# Scrapes list of courses from survey panel (obsolete)
def survey_courses(response):
    # Using Regex and Json
    import re, json
    # Search for the Json object that contains the course list and parse it
    return json.loads(re.search("json_ecb = ({.*?});", response).group(1))
