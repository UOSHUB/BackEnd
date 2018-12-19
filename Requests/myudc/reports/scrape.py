from lxml.etree import fromstring as __parse_xml

# Grade to GPA value dictionary
__to_gpa = {
    "A": 4,
    "B+": 3.5,
    "B": 3,
    "C+": 2.5,
    "C": 2,
    "D+": 1.5,
    "D": 1
}.get

# Scrapes grades and GPA from transcript report
def grades_and_gpa(transcript, term_code, known_grades=()):
    # Parse xml and declare variables
    xml = __parse_xml(transcript)
    try:
        quality = float(xml.find(".//SHRLGPA_QUALITY_POINTS").text)
        hours = int(xml.find(".//SHRLGPA_HOURS_EARNED").text)
    except AttributeError: quality, hours = 0, 0
    all_hours = hours
    term_quality = 0
    grades = []
    # Loop through the available terms in transcript
    for term in xml.find(".//LIST_G_ACADEMIC_HIST_TERM") or ():
        # If the term is the selected one
        if term.find("TERM_CODE_KEY").text == term_code:
            # Loop through courses in that term
            for course in term.find("LIST_G_ACADEMIC_HIST_DETAILS"):
                # Store its credit hours, grade and key
                crhrs = int(course.find("CREDIT_HOURS").text)
                grade = course.find("GRDE_CODE_FINAL").text
                key = course.find("SUBJ_CODE").text[-7:]
                # Add them to total hours and term quality
                all_hours += crhrs
                term_quality += __to_gpa(grade, 0) * crhrs
                # Add course's (key, title, grade, new or not) to the grades list
                grades.append((key, course.find("COURSE_TITLE").text, grade, key not in known_grades))
    # Calculate and return new grades and (term, new and old GPA)
    return grades, {
        "term": term_quality / (all_hours - hours) if all_hours != hours else 0,
        "new": (term_quality + quality) / all_hours if all_hours else 0,
        "old": quality / hours if hours else 0
    }


def remaining_courses(study_plan):
    plan = __parse_xml(study_plan)
    return {
        "crhrs": int(plan.find(".//SMBPOGN_REQ_CREDITS_OVERALL").text)
            - int(plan.find(".//SMBPOGN_ACT_CREDITS_OVERALL").text),
        "courses": [
            course.find("COURSE_NUMB1").text
            for course in plan.findall(".//G_GROUP_COURSES")
            if course.find("CF_IS_PASSED").text == "N"
        ]
    }
