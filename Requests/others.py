import requests


# Gets this year's Academic Calendar page
def academic_calendar():
    # HTTP get request from UOS homepage
    return requests.get("http://www.sharjah.ac.ae/en/academics/A-Calendar/Pages/accal17-18.aspx").text
