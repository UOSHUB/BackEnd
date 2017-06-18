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


# Scrape possible values of ["Campus", "Collage", "Department"] from offered courses report
def __values_of(courses, *params):
    # For each supported value, create an empty dictionary in values for later use
    values = {param: {} for param in params if param in ["Campus", "Collage", "Department"]}
    # Loop through courses to get the required values
    for course in __parse_xml(courses).find("LIST_G_SSBSECT_TERM_CODE"):
        # If campus values are required
        if "Campus" in values:
            # Add course's campus to values as {"campus long name": "campus abbreviation"}
            values["Campus"].update({course.find("CAMPUS_DESC").text: course.find("SSBSECT_CAMP_CODE").text})
        # If collage values are required
        if "Collage" in values:
            # Add course's collage to values as {"collage long name": "collage number"}
            values["Collage"].update({course.find("COLLEGE_NAME").text: course.find("SCBCRSE_COLL_CODE").text})
        # If department values are required
        if "Department" in values:
            # Add course's department to values as {"department long name": "department initials"}
            values["Department"].update({course.find("DEPT_NAME").text: course.find("SCBCRSE_DEPT_CODE").text})
    return values
