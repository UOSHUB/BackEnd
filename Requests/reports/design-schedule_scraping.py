from lxml.etree import fromstring as __parse_xml


# Scrapes all courses the student needs to fulfill degree reqs from study_plan
def study_plan_courses(study_plan):
    # Dictionary to store all the courses
    all_courses = {}
    # Loop through the study_plan and store their info
    for course in __parse_xml(study_plan).find(".//G_GROUP_COURSES"):
        course_id = course.find("COURSE_NUMB1").text
        course_title = course.find("GROUP_CRSE_TITLE").text
        course_credits = course.find("GROUP_CRSE_CREDITS").text
        course_grade = course.find("CF_COURSE_GRADE").text
        course_taken = course.find("CF_IS_PASSED").text
    return all_courses

def disabled_courses(all_courses):
    # Dictionary to store all the past passed courses
    past_passed_courses = {}
    # Dictionary to store all the current courses
    current_courses = {}

    # Loop through all the courses and extract the past passed courses
    for course in all_courses:
        if (course.course_taken == 'Y' & course.course_grade!= NULL):
            print("Add this passed course!")#add this course to the former dict.
        elif (course.course_taken == 'Y' & course.course_grade == NULL):
            print("Add this current course!")#add this course to the latter dict.
    return past_passed_courses, current_courses

