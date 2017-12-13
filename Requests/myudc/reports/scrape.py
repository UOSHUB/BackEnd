from lxml.etree import fromstring as __parse_xml


# Scrapes new grades from transcript report which aren't in known course
def new_grades(transcript, term_code, known_grades):
    # List to store new grades
    grades = []
    # Loop through the available terms in transcript
    for term in __parse_xml(transcript).find(".//LIST_G_ACADEMIC_HIST_TERM"):
        # If the term is the selected one
        if term.find("TERM_CODE_KEY").text == term_code:
            # Loop through courses in that term
            for course in term.find("LIST_G_ACADEMIC_HIST_DETAILS"):
                # Store course key
                course_key = course.find("SUBJ_CODE").text
                # If course isn't already among the known grades
                if course_key not in known_grades:
                    # Add its grade to the new grades list
                    grades.append((
                        # In tuple form of course (key, title, grade)
                        course_key,
                        course.find("COURSE_TITLE").text,
                        course.find("GRDE_CODE_FINAL").text
                    ))
    return grades
