from requests import post, get


def request(options):
    return post(
        url="https://uos.sharjah.ac.ae:9050/reports/rwservlet",
        data=dict({
            "server": "RptSvr_uosas5_INB_asinst",
            "desformat": "xml",
            "destype": "cache",
            "userid": "uos_mis/u_pick_it@PROD"
        }, **options)
    )


def personal_info(sid):
    response = request({
        "REPORT": "SYREXDT_REP",
        "P_SPRIDEN_ID": sid.upper()
    })
    response.encoding = "utf-8"
    return response.text.encode('utf-8')


def schedule(sid, semester):
    return request({
        "REPORT": "SYFSSCE_REP",
        "P_ID_FROM": sid.upper(),
        "P_ID_TO": sid.upper(),
        "P_TERM_CODE": semester
    }).text


def final_exams(sid, semester):
    return request({
        "REPORT": "SYRSSFE_REP",
        "P_ID": sid.upper(),
        "P_TERM_CODE": semester
    }).text


def study_plan(sid, reg_semester):
    return request({
        "REPORT": "SYRSPOS_REP",
        "P_PROG_CODE": "ALL",
        "P_EXP_GRD": "ALL",
        "P_COLL_CODE": "ALL",
        "P_CAMP_CODE": "ALL",
        "P_LEVEL_CODE": "ALL",
        "P_STUDENT_ID": sid.upper(),
        # Student enrollment semester
        "P_TERM_CODE": reg_semester
    }).text


def offered_courses(semester):
    return request({
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
    }).text


def unofficial_transcript(sid):
    return request({
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
    }).text


def academic_calendar():
    return get("http://www.sharjah.ac.ae/en/academics/A-Calendar/Pages/academiccalendar16-17.aspx").text
