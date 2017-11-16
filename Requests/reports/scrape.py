from lxml.etree import fromstring as __parse_xml


# Scrapes a specific term's schedule details
def schedule(response):
    # Dictionary to store schedule details
    details = {}
    # Loop through courses in the schedule report to get its details
    for course in __parse_xml(response).find(".//LIST_G_SSBSECT_CRN"):
        course_id = course.find("SSBSECT_SUBJ_CODE").text + course.find("SSBSECT_CRSE_NUMB").text
        # Scrape and store data dictionary in details["course id"]
        details[course_id] = {
            "crn": course.find("SSBSECT_CRN").text,
            "section": course.find("SSBSECT_SEQ_NUMB").text,
            "type": course.find("SSBSECT_SCHD_CODE").text,
            "credits": course.find("SFRSTCR_CREDIT_HR").text,
            "title": course.find("SCBCRSE_TITLE").text.strip(),
            # Initialize an empty classes array for later
            "classes": []
        }
        # Loop through days in the current course
        for day in course.find("LIST_G_DAYES"):
            # Add a class dictionary of data for every day in course
            details[course_id]["classes"].append({
                "days": day.find("DAYES").text.split(),
                "time": day.find("TIME").text.split(" - "),
                "building": day.find("SSRMEET_BLDG_CODE").text,
                "room": day.find("SSRMEET_ROOM_CODE").text,
                # Place doctors in an array as there might be many
                "doctor": [
                    doctor.find("CF_INSTRUCTOR_NAME").text
                    # Loop through doctor in the current day
                    for doctor in day.find("LIST_G_SIRASGN_PIDM")
                ]
            })
    return details


# Scrapes student's core information from his transcript
def core_details(transcript):
    # Find and store the element which contains the required info
    soup = __parse_xml(transcript).find(".//G_SGBSTDN")
    # Create a dictionary of straight forward to reach info
    details = {
        # Store student's name, college, major and terms
        "name": soup.find("STUDENT_NAME").text.strip(),
        "college": soup.find("CURR_COLL_CODE").text,
        "major": soup.find("CURR_MAJR_CODE").text,
        "terms": {
            # Initialize in progress term
            "in_progress": {},
            # Store all terms key
            "all_keys": [
                # Place term key in the array
                term.find("TERM_CODE_KEY").text
                # Loop through terms which aren't in progress
                for term in soup.find(".//LIST_G_ACADEMIC_HIST_TERM")
            ]
        },
        # Store student's first term to be used in offered_courses()
        "first_term": soup.find("FIRST_TERM_ADMIT").text
    }
    # Loop through in progress terms and keep the index of looping
    for index, term in enumerate(soup.find("LIST_G_SFRSTCR_PIDM")):
        # Add in progress term's key to all terms key
        details["terms"]["all_keys"].append(term.find("SFRSTCR_TERM_CODE").text)
        # If it's the first in progress term
        if index == 0:
            # Store its key and courses as the "in_progress" term
            details["terms"]["in_progress"][term.find("SFRSTCR_TERM_CODE").text] = {
                # Combine course's subject code and section code to get its key
                course.find("SSBSECT_SUBJ_CODE").text + course.find("SSBSECT_CRSE_NUMB").text:
                    # With the line above, form {"course key": "course name"} pairs
                    course.find("SFRSTCR_COURSE_TITLE").text.strip()
                # Loop through courses in that term
                for course in term.find("LIST_G_SFRSTCR_DETAIL")
            }
    return details


# Scrapes new grades from transcript report which aren't in known course
def new_grades(transcript, term_key, known_courses):
    # Dictionary to store new grades
    grades = {}
    # Loop through the available terms in transcript
    for term in __parse_xml(transcript).find(".//LIST_G_ACADEMIC_HIST_TERM"):
        # If the term is the selected one
        if term.find("TERM_CODE_KEY").text == term_key:
            # Loop through courses in that term
            for course in term.find("LIST_G_ACADEMIC_HIST_DETAILS"):
                # Store course title
                course_title = course.find("COURSE_TITLE").text
                # If course isn't already among the known courses
                if course_title not in known_courses:
                    # Add its grade to the new grades dictionary
                    grades[course_title] = course.find("GRDE_CODE_FINAL").text
    return grades
