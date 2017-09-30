from lxml.html import fromstring as __parse
import requests

seasons_codes = {
    "10": "Fall Semester",
    "20": "Spring Semester",
    "30": "Summer Session"
}


# Gets this year's Academic Calendar page
def academic_calendar():
    # HTTP get request from UOS homepage
    return requests.get("http://www.sharjah.ac.ae/en/academics/A-Calendar/Pages/accal17-18.aspx").text


# Scrapes specified term's calendar events
def term_events(response, term_code):
    # Initialize events array
    events = []
    # Store term's year
    year = term_code[:4]
    # Format term name in "Fall Semester 2017/2017" format from term code
    term_name = "{} {}/{}".format(seasons_codes[term_code[4:]], year, int(year) + 1)
    # Loop through available terms calendars
    for term in __parse(response).findall(".//div[@class='pageTurn']/div/div"):
        # If calendar's label matches requested term name
        if term.find("label").text == term_name:
            # Loop through it's events (table rows)
            for event in term.findall(".//tbody/tr"):
                # Store event row's cells
                cells = event.findall("td")
                # Add event's date and text to events array
                events.append({
                    "date": cells[2].text,
                    "text": cells[4].text_content().strip()
                })
            return events
