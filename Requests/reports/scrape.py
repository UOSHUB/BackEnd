from lxml.etree import fromstring as __parse_xml


# Scrapes new grades from transcript that aren't in known course
def new_grades(transcript, semester, known_courses):
    # Dictionary to store new grades
    grades = {}
    # Loop through the available semesters in transcript
    for term in __parse_xml(transcript).find(".//LIST_G_ACADEMIC_HIST_TERM"):
        # If the semester is the selected one
        if term.find("TERM_TERM_DESC").text == semester:
            # Loop through courses in that semester
            for course in term.find("LIST_G_ACADEMIC_HIST_DETAILS"):
                # Store course title
                course_title = course.find("COURSE_TITLE").text
                # If course isn't already among the known courses
                if course_title not in known_courses:
                    # Add it's grade to the new grades dictionary
                    grades[course_title] = course.find("GRDE_CODE_FINAL").text
    return grades
