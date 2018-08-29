from .get import page, __root_url, requests
from .scrape import __parse

# Gets student's directory profile page
def dir_profile(session):
    # Coming from "Personal Information" page
    return page("bwgkoprf.P_ShowDiroItems", "GenMnu", session)


# Gets student's account summary page
# ether all terms combined or one by one (by_term=True)
def account_summary(session, by_term=False):
    # Coming from "Student Account" page
    return page("bwskoacc.P_ViewAcct" + ["Total", ''][by_term], "ARMnu", session)


# Gets student's admission application details page
def admission_card(session):
    # Coming from "My Admission" page
    return page("uos_admission_card.p_dispadmissioncard", "MyAdmMnu", session)


def all_offered_courses(session):
    return offered_courses_select(session, [
        "0001", "0103", "0104", "0201", "0202", "0203", "0204", "0205", "0206", "0301", "0302", "0303", "0306",
        "0307", "0308", "0401", "0402", "0403", "0404", "0405", "0406", "0407", "0408", "0500", "0501", "0502",
        "0503", "0504", "0505", "0506", "0507", "0601", "0602", "0603", "0800", "0803", "0806", "0807", "0808",
        "0900", "1102", "1101", "1103", "1104", "1105", "1202", "1203", "1204", "1206", "1211", "1212", "1213",
        "1410", "1411", "1412", "1420", "1426", "1427", "1430", "1440", "1450"
    ])


def offered_courses_select(session, subjects):
    return requests.get(
        # Get data from root url + sub url
        __root_url + "bwskfcls.P_GetCrse",
        params=[
            *[(param, "") for param in [
                "sel_day", "sel_schd", "sel_insm", "sel_camp", "sel_levl", "sel_ptrm",
                "sel_sess", "sel_instr", "sel_attr", "sel_subj", "sel_crse", "sel_title",
                "begin_hh", "begin_mi", "end_hh", "end_mi", "begin_ap", "end_ap", "path", "rsts", "crn"
            ]],
            *[("sel_subj", subject) for subject in subjects],
            ("SUB_BTN", "Course Search"),
            ("term_in", "201810"),
        ],
        # Coming from "referer" page (required by myUDC)
        headers={"referer": __root_url + "bwckgens.p_proc_term_date"},
        # Send login session
        cookies=session
    ).text


# TODO: Finish implementing these functions
def registrable_courses_from_all(page, subjects):
    courses = []
    # Loop through finals table's rows which contain data
    for section in __parse(page).findall(".//table[@class='datadisplaytable']")[1:]:
        # Store final's row cells
        subject = section.find("./tr[2]/th").text[:4]
        if subject in subjects:
            for course in section.findall(".//form[@action='/prod_enUS/bwskfcls.P_GetCrse']"):
                courses.append(subject)
    return courses


def registrable_courses(page):
    courses = []
    # Loop through finals table's rows which contain data
    for course in __parse(page).findall(".//form[@action='/prod_enUS/bwskfcls.P_GetCrse']"):
        # Store final's row cells
        rows = course.findall("tr")
        if len(rows) <= 2: continue
        subject = rows[1].find("th").text
        print(subject)
    return courses


# Gets student's basic info from admission card page
def student_details(page):
    # Extract tables from page and store major's table
    tables = __parse(page).findall(".//table[@class='datadisplaytable']/tr")
    major = tables[3].findall("./td")
    # Return student's origin, collage and major
    return {
        "origin": tables[1].findall("./td")[2].text,
        "college": major[1].text,
        "major": major[2].text
    }
