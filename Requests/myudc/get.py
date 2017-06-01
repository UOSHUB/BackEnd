import requests

root_url = "https://uos.sharjah.ac.ae:9050/prod_enUS/"


def __login(sid, pin):
    return requests.post(
        root_url + "twbkwbis.P_ValLogin",
        data={"sid": sid, "PIN": pin},
        cookies={"TESTID": "set"}
    ).cookies


def transcript(session):
    return requests.post(
        root_url + "bwskotrn.P_ViewTran",
        data={"tprt": "NOF"},
        headers={"referer": root_url + "bwskotrn.P_ViewTermTran"},
        cookies=session
    ).text


def get_page(link, referer, session):
    return requests.get(
        root_url + link,
        headers={"referer": root_url + "twbkwbis.P_GenMenu?name=bmenu.P_" + referer},
        cookies=session
    ).text


def active_reg(session):
    return get_page("bwsksreg.p_active_regs", "RegMnu", session)


def holds(session):
    return get_page("bwskoacc.P_ViewHold", "AdminMnu", session)


def account_summary(session, by_term=False):
    return get_page("bwskoacc.P_ViewAcct" + ["Total", ''][by_term], "ARMnu", session)


def admission_card(session):
    return get_page("uos_admission_card.p_dispadmissioncard", "MyAdmMnu", session)


def __dir_profile(session):
    return get_page("bwgkoprf.P_ShowDiroItems", "GenMnu", session)
