import requests

# Root url of myUDC
__root_url = "https://uos.sharjah.ac.ae:9050/prod_enUS/"


# Gets student's schedule page by term code
def term(term_code, session):
    return requests.post(
        # Get data from detail schedule url
        __root_url + "bwskfshd.P_CrseSchdDetl",
        # Send required term code
        data={"term_in": term_code},
        # Coming from the same page
        headers={"referer": __root_url + "bwskfshd.P_CrseSchdDetl"},
        # Send login session
        cookies=session
    ).text


# Gets student's unofficial transcript page
def transcript(session):
    return requests.post(
        # Get data from academic transcript url
        __root_url + "bwskotrn.P_ViewTran",
        # Get "Non Official Transcript"
        data={"tprt": "NOF"},
        # Coming from "Academic Transcript Options" page
        headers={"referer": __root_url + "bwskotrn.P_ViewTermTran"},
        # Send login session
        cookies=session
    ).text


# TODO: test this function on all courses in advanced search
# Gets a single course's details using its course key, crn and term
def course(session, crn, course_key, term_code):
    return requests.get(
        # Get data from display course url
        __root_url + "bwckschd.p_disp_listcrse",
        # Coming from "Advanced Search" page
        headers={"referer": __root_url + "bwskfcls.P_GetCrse_Advanced"},
        # Send all course identifiers
        params={
            "term_in": term_code,
            "subj_in": course_key[:4],
            "crse_in": course_key[4:],
            "crn_in": crn
            # Send login session
        }, cookies=session
    ).text


# General myUDC page request with common attributes
def page(link, referer, session):
    return requests.get(
        # Get data from root url + sub url
        __root_url + link,
        # Coming from "referer" page (required by myUDC)
        headers={"referer": __root_url + "twbkwbis.P_GenMenu?name=bmenu.P_" + referer},
        # Send login session
        cookies=session
    ).text


# Gets student's active registration page
def active_reg(session):
    # Coming from "Registration" page
    return page("bwsksreg.p_active_regs", "RegMnu", session)


# Gets student's registration history page
def reg_history(session):
    # Coming from "Registration" page
    return page("bwskhreg.p_reg_hist", "RegMnu", session)


# Gets student's holds page
def holds(session):
    # Coming from "Student Records" page
    return page("bwskoacc.P_ViewHold", "AdminMnu", session)


# Gets student's final exams page for a specific term
def final_exams(session, term_code):
    return page(
        # Request exams schedule coming from "Registration" page
        "uos_dispexam.P_DispExamSchdSum", "RegMnu",
        # Select term and send it's cookies as the session
        requests.post(
            # Send selected term to be stored
            __root_url + "bwcklibs.P_StoreTerm",
            # Send required term code
            data={"term_in": term_code},
            # Coming from the "Select Term" page
            headers={"referer": __root_url + "bwskflib.P_SelDefTerm"},
            # Send a copy of login session
            cookies=session
        ).cookies.get_dict()
    )


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


# Gets student's admission application details page
def admission_card(session):
    # Coming from "My Admission" page
    return page("uos_admission_card.p_dispadmissioncard", "MyAdmMnu", session)
