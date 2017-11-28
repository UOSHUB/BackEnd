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


# Gets student's account summary page
# ether all terms combined or one by one (by_term=True)
def account_summary(session, by_term=False):
    # Coming from "Student Account" page
    return page("bwskoacc.P_ViewAcct" + ["Total", ''][by_term], "ARMnu", session)


# Gets student's admission log card page
def admission_card(session):
    # Coming from "My Admission" page
    return page("uos_admission_card.p_dispadmissioncard", "MyAdmMnu", session)
