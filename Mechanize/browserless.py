import requests

url = "{}://{}.sharjah.{}/reports/rwservlet"
common = {
    "desformat": "xml",
    "destype": "cache",
    "userid": "uos_mis/u_pick_it@PROD",
}


def study_plan(sid):
    return requests.post(url.format("http", "uosas5", "uos.edu:7782"), data=dict({
        "REPORT": "SYRSPOS_REP",
        "P_TERM_CODE": "201410",
        "P_PROG_CODE": "ALL",
        "P_EXP_GRD": "ALL",
        "P_COLL_CODE": "ALL",
        "P_CAMP_CODE": "ALL",
        "P_LEVEL_CODE": "ALL",
        "P_STUDENT_ID": sid.upper()
    }, **common)).text


def personal_info(sid):
    request = requests.post(url.format("https", "uos", "ac.ae:9050"), data=dict({
        "REPORT": "syrexdt_rep.rep",
        "server": "RptSvr_uosas5_INB_asinst",
        "P_SPRIDEN_ID": sid.upper()
    }, **common))
    request.encoding = "utf-8"
    return request.text


def academic_calendar():
    return requests.get("http://www.sharjah.ac.ae/en/academics/A-Calendar/Pages/academiccalendar16-17.aspx").text
