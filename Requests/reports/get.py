import requests


# General report request with common attributes
def report(options):
    # HTTP post request
    return requests.post(
        # Root UOS reports url
        url="https://uos.sharjah.ac.ae:9050/reports/rwservlet",
        # Parameters used across all report requests
        data=dict({
            # Request from UOS server
            "server": "RptSvr_uosas5_INB_asinst",
            # Get report in XML format
            "desformat": "xml",
            # Cache the report until it's processed
            "destype": "cache",
            # User id of reports server
            "userid": "uos_mis/u_pick_it@PROD"
            # Append report specific extra parameters
        }, **options)
    )


# Gets student's personal information
def personal_info(sid):
    return report({
        # Report cipher
        "REPORT": "SYREXDT_REP",
        # Student id
        "P_SPRIDEN_ID": sid.upper()
        # Encode content in utf-8 as it contains Arabic
    }).content.decode()


# Gets student's summarized schedule
def schedule(sid, term):
    return report({
        # Report cipher
        "REPORT": "SYFSSCE_REP",
        # Student ids range (from, to)
        "P_ID_FROM": sid.upper(),
        "P_ID_TO": sid.upper(),
        # term code
        "P_TERM_CODE": term
    }).content


# Gets student's final exams schedule
def final_exams(sid, term_code):
    return report({
        # Report cipher
        "REPORT": "SYRSSFE_REP",
        # Student id
        "P_ID": sid.upper(),
        # term code
        "P_TERM_CODE": term_code
    }).content


# Gets student's whole study plan
def study_plan(sid, reg_term_code):
    return report({
        # Report cipher
        "REPORT": "SYRSPOS_REP",
        # Still don't know these two
        "P_PROG_CODE": "ALL",
        "P_EXP_GRD": "ALL",
        # Collage number
        "P_COLL_CODE": "ALL",
        # Campus abbreviation
        "P_CAMP_CODE": "ALL",
        # Degree level initials
        "P_LEVEL_CODE": "ALL",
        # Student id
        "P_STUDENT_ID": sid.upper(),
        # Student enrollment term code
        "P_TERM_CODE": reg_term_code
    }).content


# Gets offered courses catalog for a term
def offered_courses(department="%", term_code="201720"):
    return report({
        # Report cipher
        "REPORT": "SYRSCHE_REP",
        # Campus abbreviation
        "CAMP": "%",
        # Collage number
        "COLL": "%",
        # Department short name
        "DEPT": department,
        # Degree level initials
        "LEVL": "ALL",
        # Major registration restrictions
        "P_IND": "ALL",
        # Availability for web add/drop
        "P_WEB": "Y",
        # Class capacity range (min, max)
        "MAX": "258",
        "MIN": "0",
        # term code
        "TERM": term_code
    }).content


# Gets student's unofficial transcript
def unofficial_transcript(sid):
    return report({
        # Report cipher
        "REPORT": "SYFTRTE_REP",
        # Campus abbreviation
        "P_CAMP": "ALL",
        # Degree level initials
        "P_LEVL_CODE": "ALL",
        # Collage number
        "P_COLL_CODE": "ALL",
        # Still don't know these three
        "P_NATION_CODE": "ALL",
        "P_SPONSOR_ID": "ALL",
        "P_EXP_GRD": "ALL",
        # Whether to show in progress courses
        "P_INPROG_CRS_IND": "Y",
        # Student id
        "P_ID": sid.upper()
    }).content
