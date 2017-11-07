from lxml.etree import fromstring as __parse_xml


# Scrapes all courses the student needs to fulfill degree reqs from study_plan
def study_plan_courses(study_plan):
    # Dictionary to store all the courses
    all_courses = set()
    # Loop through the study_plan and store their info
    for term in __parse_xml(study_plan).findall(".//LIST_G_GROUP_COURSES"):
        for course in term:
            if course.find("CF_IS_PASSED").text == 'N':
                all_courses.add(course.find("COURSE_NUMB1").text)

    return all_courses