# Import two html processing functions as hidden variables
from lxml.html import fromstring as __parse_html, tostring as __get_html


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


# Scraps url of Blackboard profile image
def profile_image(response):
    return __parse_html(response).xpath("//a[@id='profileLink']/img/@src")[0]
