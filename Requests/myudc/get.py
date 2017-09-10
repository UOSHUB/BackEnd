import requests

# Root url of myUDC
root_url = "https://uos.sharjah.ac.ae:9050/prod_enUS/"


# Logs in myUDC and returns the session
def __login(sid, pin):
    return requests.post(
        # Post data to login url
        root_url + "twbkwbis.P_ValLogin",
        # Send student id and password
        data={"sid": sid, "PIN": pin},
        # Required cookie for myUDC login
        cookies={"TESTID": "set"}
    ).cookies.get_dict()


# Gets student's schedule page by term id
def schedule(term, session):
    return requests.post(
        # Get data from detail schedule url
        root_url + "bwskfshd.P_CrseSchdDetl",
        # Send required term id
        data={"term_in": term},
        # Coming from the same page page
        headers={"referer": root_url + "bwskfshd.P_CrseSchdDetl"},
        # Send login session
        cookies=session
    ).text


# Gets student's unofficial transcript page
def transcript(session):
    return requests.post(
        # Get data from academic transcript url
        root_url + "bwskotrn.P_ViewTran",
        # Get "Non Official Transcript"
        data={"tprt": "NOF"},
        # Coming from "Academic Transcript Options" page
        headers={"referer": root_url + "bwskotrn.P_ViewTermTran"},
        # Send login session
        cookies=session
    ).text


# General myUDC page request with common attributes
def page(link, referer, session):
    return requests.get(
        # Get data from root url + sub url
        root_url + link,
        # Coming from "referer" page (required by myUDC)
        headers={"referer": root_url + "twbkwbis.P_GenMenu?name=bmenu.P_" + referer},
        # Send login session
        cookies=session
    ).text


# Gets student's active registration page
def active_reg(session):
    # Coming from "Registration" page
    return page("bwsksreg.p_active_regs", "RegMnu", session)


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
