from Requests.myudc import root_url as __root_url
import requests

# URL of MyUDC reports (extracted from MyUDC root URL)
__url = __root_url[:-10] + "reports/rwservlet"
_format = "xml"

# General report request with common attributes
def report(options):
    # HTTP post request
    return requests.post(
        # UOS reports url & options used across all requests
        url=__url, data=dict({
            # Request from UOS server
            "server": "RptSvr_uosas5_INB_asinst",
            # Get report in specified format
            "desformat": _format,
            # Cache the report until it's processed
            "destype": "cache",
            # User id of reports server
            "userid": "uos_mis/u_pick_it@PROD"
            # Append report specific extra parameters
        }, **options)
    )


# Gets student's unofficial transcript
def unofficial_transcript(sid, *_):
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


# Gets student's whole study plan
def study_plan(sid, *_):
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
        # Student enrollment term code (extracted from student id)
        "P_TERM_CODE": '20' + (sid[1:4] if sid[1] != '0' else '141') + '0'
    }).content


# Gets student's personal information
def personal_information(sid, *_):
    return report({
        # Report cipher
        "REPORT": "SYREXDT_REP",
        # Student id
        "P_SPRIDEN_ID": sid.upper()
        # Encode content in utf-8 as it contains Arabic
    }).content.decode()


# Gets student's summarized schedule
def summarized_schedule(sid, term_code):
    return report({
        # Report cipher
        "REPORT": "SYFSSCE_REP",
        # Student ids range (from, to)
        "P_ID_FROM": sid.upper(),
        "P_ID_TO": sid.upper(),
        # term code
        "P_TERM_CODE": term_code,
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


# Gets offered courses catalog for a term
def offered_courses(_, term_code):
    return report({
        # Report cipher
        "REPORT": "SYRSCHE_REP",
        # Campus abbreviation
        "CAMP": "%",
        # Collage number
        "COLL": "%",
        # Department short name
        "DEPT": "%",
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
