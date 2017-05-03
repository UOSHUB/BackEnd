import requests

url = "{}://{}.sharjah.{}/reports/rwservlet"
common = {
    "desformat": "xml",
    "destype": "cache",
    "userid": "uos_mis/u_pick_it@PROD",
}


def academic_calendar():
    return requests.get("http://www.sharjah.ac.ae/en/academics/A-Calendar/Pages/academiccalendar16-17.aspx").text


def personal_info(sid):
    request = requests.post(url.format("https", "uos", "ac.ae:9050"), data=dict({
        "REPORT": "syrexdt_rep",
        "server": "RptSvr_uosas5_INB_asinst",
        "P_SPRIDEN_ID": sid.upper()
    }, **common))
    request.encoding = "utf-8"
    return request.text


def uosas5_request(options):
    return requests.post(url.format("http", "uosas5", "uos.edu:7782"), data=dict(options, **common)).text


def study_plan(sid):
    return uosas5_request({
        "REPORT": "SYRSPOS_REP",
        # Student enrollment semester
        "P_TERM_CODE": "201410",
        "P_PROG_CODE": "ALL",
        "P_EXP_GRD": "ALL",
        "P_COLL_CODE": "ALL",
        "P_CAMP_CODE": "ALL",
        "P_LEVEL_CODE": "ALL",
        "P_STUDENT_ID": sid.upper()
    })


def offered_courses(semester):
    return uosas5_request({
        "REPORT": "SYRSCHE_REP",
        "CAMP": "%",
        "COLL": "%",
        "DEPT": "%",
        "LEVL": "ALL",
        "P_IND": "ALL",
        "P_WEB": "ALL",
        "MAX": "258",
        "MIN": "0",
        "TERM": semester
    })


def unofficial_transcript(sid):
    return uosas5_request({
        "REPORT": "SYFTRTE_REP",
        "P_CAMP": "ALL",
        "P_LEVL_CODE": "ALL",
        "P_COLL_CODE": "ALL",
        "P_NATION_CODE": "ALL",
        "P_SPONSOR_ID": "ALL",
        "P_EXP_GRD": "ALL",
        # Whether to show in progress courses
        "P_INPROG_CRS_IND": "Y",
        "P_ID": sid.upper()
    })
