import requests


def academic_calendar():
    return requests.get("http://www.sharjah.ac.ae/en/academics/A-Calendar/Pages/academiccalendar16-17.aspx").text
