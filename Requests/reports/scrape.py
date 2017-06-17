from lxml.etree import fromstring as __parse_xml


# Scrapes new grades from transcript report which aren't in known course
def new_grades(transcript, semester, known_courses):
    # Dictionary to store new grades
    grades = {}
    # Loop through the available semesters in transcript
    for term in __parse_xml(transcript).find(".//LIST_G_ACADEMIC_HIST_TERM"):
        # If the semester is the selected one
        if term.find("TERM_CODE_KEY").text == semester:
            # Loop through courses in that semester
            for course in term.find("LIST_G_ACADEMIC_HIST_DETAILS"):
                # Store course title
                course_title = course.find("COURSE_TITLE").text
                # If course isn't already among the known courses
                if course_title not in known_courses:
                    # Add it's grade to the new grades dictionary
                    grades[course_title] = course.find("GRDE_CODE_FINAL").text
    return grades


# Scrapes campus abbreviations from offered courses report
def __campus_abbreviations(courses):
    # Using a pythonic short loop
    return {
        # Create {key: value} pairs of {"campus long name": "campus abbreviation"}
        course.find("CAMPUS_DESC").text: course.find("SSBSECT_CAMP_CODE").text
        # Loop through courses to get campuses (as courses are offered in different campuses)
        for course in __parse_xml(courses).find("LIST_G_SSBSECT_TERM_CODE")
    }


# Scrapes collages numbers from offered courses report
def __collages_numbers(courses):
    # Using a pythonic short loop
    return {
        # Create {key: value} pairs of {"collage long name": "collage number"}
        course.find("COLLEGE_NAME").text: course.find("SCBCRSE_COLL_CODE").text
        # Loop through courses to get collages (as courses are offered by different collages)
        for course in __parse_xml(courses).find("LIST_G_SSBSECT_TERM_CODE")
    }


# Scrapes departments initials from offered courses report
def __departments_initials(courses):
    # Using a pythonic short loop
    return {
        # Create {key: value} pairs of {"department long name": "department initials"}
        course.find("DEPT_NAME").text: course.find("SCBCRSE_DEPT_CODE").text
        # Loop through courses to get departments (as courses are offered by different departments)
        for course in __parse_xml(courses).find("LIST_G_SSBSECT_TERM_CODE")
    }
