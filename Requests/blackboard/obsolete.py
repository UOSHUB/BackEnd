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


# Get direct list of courses
def get_courses(session):
    # Get data from top right navigation menu
    return data("blackboard/execute/globalCourseNavMenuSection", session, {
        # Required parameter
        "cmd": "view"
    })


# Scrapes courses ids from list_of("Courses") and courses()
def scrape_courses(response, from_list_of=False):
    from lxml.html import fromstring as parse_html
    # Determine scraped attribute and location of course id
    # depending on whether the sent data is from list_of() or courses() functions
    attr, start, end = ("href", 54, -7) if from_list_of else ("onclick", 87, -24)
    # Return dictionary of courses blackboard ids mapped to courses myUDC ids
    return {link.text[:7]: link.attrib[attr][start:end] for link in parse_html(response).xpath("//a")}


# Scrapes list of courses from survey panel
def survey_courses(response):
    # Using Regex and Json
    import re, json
    # Search for the Json object that contains the course list and parse it
    return json.loads(re.search("json_ecb = ({.*?});", response).group(1))
