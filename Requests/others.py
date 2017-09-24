from lxml.html import fromstring as __parse, tostring
import requests


# Gets this year's Academic Calendar page
def academic_calendar():
    # HTTP get request from UOS homepage
    return requests.get("http://www.sharjah.ac.ae/en/academics/A-Calendar/Pages/accal17-18.aspx").text


# Scraping
def get_semcal(tdata, sem_id):
    sem_data = []
    seasons_codes = {"10": "Fall Semester", "20": "Spring Semester", "30": "Summer Session"}
    season = seasons_codes[sem_id[4:]]
    year = sem_id[:4]
    yearpp = int(year) + 1
    term = "{} {}/{}".format(season, year, yearpp)
    for sems in __parse(tdata).findall(".//div[@class='pageTurn']/div/div"):
        if sems.find("label").text == term:
            for day in sems.findall("div/table/tbody/tr"):
                day_tds = day.findall("td")
                day_data ={"date":day_tds[2].text,"desc":day_tds[4].text_content().strip()}
                sem_data.append(day_data)
            return sem_data
