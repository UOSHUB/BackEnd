from lxml.html import fromstring as __parse_html, tostring as __get_html
from lxml.etree import fromstring as __parse_xml
from .general import root_url, web, mobile, api, __id
from .values import __terms
from math import ceil
import requests


# Logs in Blackboard and returns the session
def login(sid, pin):
    # Post HTTP request and store its response
    response = requests.post(
        # Post data to login url
        root_url + "webapps/login/",
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


# Gets a list of items through AJAX
def list_of(session, query):
    # Get data from AJAX requests url
    return web("portal/execute/tabs/tabAction", session, {
        # Get list through AJAX
        "action": "refreshAjaxModule",
        # Get list of one of these options
        "modId": __id({
            "Announcements": 1,
            "Courses": 4,
            "Organizations": 5,
            "Tasks": 7,
            "Notes": 12,
            "Grades": 20,
            "Collages": 28,
            "Surveys": 257
        }[query]),
        # Required parameter
        "tabId": __id(1),
    })


# Gets page of announcements for all courses or for one course by id
def get_announcements(session, course_id=None):
    # Get data from announcements url
    return web("blackboard/execute/announcement", session, {
        # By default get all course announcements, if course id is sent then only get the sent one
        "method": "search", "searchSelect": course_id or "announcement.coursesonly.label"
    }).text


# Scrapes announcements' useful data from the web
def scrape_announcements(response):
    # Parse page's html and store it
    page = __parse_html(response)
    # Store course ids dictionary
    ids = {
        # Store values in {course name: course id} pairs
        course.text[1:]: course.get("value")
        # Loop through student's available courses
        for course in page.findall(".//select[@id='searchSelectId']/option")[3:]
    }
    # Array to store announcements dictionaries
    messages = []
    # Loop through announcements
    for item in page.findall(".//ul[@id='announcementList']/li"):
        # Add announcement to the array
        messages.append({
            # Clear announcement title from white spaces and store it
            "title": item.find("h3[@class='item']").text.strip(),
            # Store raw announcement body in html format after encoding in utf-8
            "body": __get_html(item.find(".//div[@class='vtbegenerated']")).decode(),
            # Store announcement date from first paragraph in ".details" tag
            "date": item.find("div[@class='details']/p/span").text[11:],
            # Store announcement's associated course id
            "id": ids[item.find("div[@class='announcementInfo']/p[2]").text_content()[11:]],
        })
    return messages


# Gets course's specific menu (on the left side)
def course_menu(session, course_id):
    # Get data from course menu url
    return web("blackboard/content/courseMenu.jsp", session, {
        # Specify requested course id
        "course_id": __id(course_id)
    })


# Gets a specific course's data by its id
def course_data(session, course_id, section):
    # Get data from course data url
    return mobile("courseData", session, {
        # Send course id
        "course_id": __id(course_id),
        # Currently known possible values are
        # "ANNOUNCEMENTS" and "GRADES"
        "course_section": section,
        # This flag reduces HTML junk
        "rich_content_level": "RICH"
    })


# Get student's list of courses
def get_courses_list(session, sid):
    # Get student's courses while passing his id
    return api("users/userName:" + sid + "/courses", session, {
        # Only return the field "created" and sort by it
        "fields": "created,courseId,courseRoleId"
    })


# Scrapes student's list of courses
def scrape_courses_list(response, term_code):
    # Store term year and months range start and end
    start, end = __terms[term_code[4:]]["range"]
    year = term_code[:4]
    return [
        # Return an array of courses ids
        course["courseId"][1:-2]
        # Get and loop through student's latest 10 courses
        for course in response["results"][-10:]
        # Only return courses from requested year
        if course["created"][:4] == year and
        # And in the range of months of requested term
        start >= int(course["created"][5:7]) >= end and
        # And which role is 'Student'
        course["courseRoleId"] == "Student"
    ]


# Get student's current term code
def current_term(session, sid):
    # Get student's courses while passing his id
    date = api("users/userName:" + sid + "/courses", session, {
        # Only return the field "created" and sort by it
        "fields": "created",
        "sort": "created"
        # Select student's latest course creation date
    })["results"][-1]["created"]
    # Extract term code by concatenating year and semester code according to the month
    return date[:4] + (int(date[6]) > 7 and "10" or date[6] < "6" and "20" or "30")


# Gets the tasks page
def tasks(session):
    # Get data from tasks management page
    return web("blackboard/execute/taskEditList", session)


# Get direct list of courses
def get_courses(session):
    # Get data from top right navigation menu
    return web("blackboard/execute/globalCourseNavMenuSection", session, {
        # Required parameter
        "cmd": "view"
    })


# Scrapes courses ids from list_of("Courses")
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


# Gets student's specific course grades
def get_course_grades(session, course_id):
    # Request form Blackboard Mobile
    return mobile(
        # Get data from course data url
        "courseData", session, {
            # Specify section as "grades"
            "course_section": "GRADES",
            # Specify requested course id
            "course_id": __id(course_id)
        }
    )


# Scrapes student's specific course grades
def scrape_course_grades(response, course_key):
    grades = []
    # Loop through grades in available in course
    for grade in __parse_xml(response).find("grades"):
        print(grade.get("name"))
        # Store last modified time
        time = grade.get("lastInstructorActivity")
        # If it's a graded items
        if time:
            # Add grade dictionary to grades
            grades.append({
                # Add item's title, grade & course key
                "course": course_key,
                "title": grade.get("name"),
                "grade": ceil(float(grade.get("grade"))),
                # Add total grade and uploaded time
                "outOf": ceil(float(grade.get("pointspossible"))),
                "time": time
            })
    return grades
