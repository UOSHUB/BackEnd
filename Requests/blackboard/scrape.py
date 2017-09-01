# Import two html processing functions as hidden variables
from lxml.html import fromstring as __parse_html, tostring as __get_html
from .values import __types, __events


# Scrapes useful data from updates JSON object
def updates(response):
    # Dictionary to store data
    data = {"courses": {
        # Loop through courses and store their name and id
        course["id"]: course["name"] for course in response["sv_extras"]["sx_courses"]
    }, "updates": []}
    # Loop through updates
    for update in response["sv_streamEntries"]:
        # Store repeatedly used references of the object
        event = update["extraAttribs"]["event_type"].split(":")
        item = update["itemSpecificData"]
        details = item["notificationDetails"]
        # Append update dictionary to data
        data["updates"].append({
            # Store all ids related to the update
            "updateId": details["actorId"],
            "courseId": details["courseId"],
            "contentId": details["sourceId"],
            # Store title and time
            "title": item["title"],
            "time": update["se_timestamp"],
            # Get meaningful equivalent of event from stored values
            "event": __types[event[0]] + " " + __events[event[1].split('_')[-1]]
        })
    return data


# Scrapes courses ids from list_of("Courses") and courses()
def courses(response, from_list_of=False):
    # Determine scraped attribute and location of course id
    # depending on whether the sent data is from list_of() or courses() functions
    attr, start, end = ("href", 54, -7) if from_list_of else ("onclick", 87, -24)
    # Return dictionary of courses blackboard ids mapped to courses myUDC ids
    return {link.text[:7]: link.attrib[attr][start:end] for link in __parse_html(response).xpath("//a")}


# Scrapes announcements' useful data
def announcements(response):
    # Array to store announcements dictionaries
    messages = []
    # Loop through announcements
    for item in __parse_html(response).xpath("//ul[@id='announcementList']/li"):
        # Add announcement to the array
        messages.append({
            # Clear announcement title from white spaces and store it
            "title": item.xpath("h3[@class='item']")[0].text.strip(),
            # Store raw announcement body in html format after encoding in utf-8
            "body": __get_html(item.xpath(".//div[@class='vtbegenerated']")[0]).decode(),
            # Store tag's all children text content as date using text_content()
            "date": item.xpath("div[@class='details']/p")[0].text_content(),
            # Store announcement's associated course id
            "id": item.xpath(".//span[@class='courseId']")[0].text[:7],
        })
    return messages
