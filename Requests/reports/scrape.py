from lxml.etree import fromstring as __parse_xml


def new_grades(transcript, semester, known_courses):
    grades = {}
    for term in __parse_xml(transcript).find(".//LIST_G_ACADEMIC_HIST_TERM"):
        if term.find("TERM_TERM_DESC").text == semester:
            for course in term.find("LIST_G_ACADEMIC_HIST_DETAILS"):
                course_title = course.find("COURSE_TITLE").text
                if course_title not in known_courses:
                    grades[course_title] = course.find("GRDE_CODE_FINAL").text
    return grades
