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


# Scrapes all courses the student needs to fulfill degree reqs from study_plan
def next_semester_courses(offered_courses, remaining_courses):
    # Dictionary to store all the courses
    future_options = {}
    # Loop through the offered_courses and store their info
    for courses in __parse_xml(offered_courses).findall(".//LIST_G_COURSE_NO"):
        for course in courses:
            id = (course.find("COURSE_NO").text).replace("-", "")
            if(id in remaining_courses):
                course_details = {}
                course_details["CRN"] = (course.find("SSBSECT_CRN").text)
                course_details["title"] = (course.find("SCBCRSE_TITLE").text)
                course_details["crd_hr"] = (course.find("SCBCRSE_CREDIT_HR_LOW").text)
                course_details["max"] = (course.find("SSBSECT_MAX_ENRL").text)
                course_details["actual"] = (course.find("SSBSECT_ENRL").text)
                sec_no = 0

                for section in __parse_xml(offered_courses).findall(".//LIST_G_SSBSECT_SCHD_CODE"):
                    section_details = {}
                    section_details["building"] = (course.find(".//SSRMEET_BLDG_CODE").text)
                    section_details["room"] = (course.find(".//SSRMEET_ROOM_CODE").text)
                    section_details["time"] = (course.find(".//TIME").text)
                    section_details["days"] = (course.find(".//DAYES").text)
                    #course_details["instructor"] = (course.find(".//SSRMEET_BLDG_CODE").text)
                    course_details["section_" + str(sec_no+1)] = section_details

                future_options[id] = course_details


    return future_options