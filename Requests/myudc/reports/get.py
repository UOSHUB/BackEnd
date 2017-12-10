from Requests.myudc import root_url as __root_url
import requests

# URL of MyUDC reports (extracted from MyUDC root URL)
__url = __root_url[-10] + "reports/rwservlet"


# General report request with common attributes
def report(options):
    # HTTP post request
    return requests.post(
        # UOS reports url & options used across all requests
        url=__url, data=dict({
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
