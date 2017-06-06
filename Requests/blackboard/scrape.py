from lxml.html import fromstring as __parse_html, tostring as __get_html


def courses(response, from_list_of=False):
    return {
        link.text[:7]: from_list_of and link.attrib["href"][54:-7] or link.attrib["onclick"][87:-24]
        for link in __parse_html(response).xpath("//a")
    }


def announcements(response):
    messages = []
    for item in __parse_html(response).xpath("//ul[@id='announcementList']/li"):
        messages.append({
            "title": item.xpath("h3[@class='item']")[0].text.strip(),
            "body": __get_html(item.xpath(".//div[@class='vtbegenerated']")[0]).decode(),
            "date": item.xpath("div[@class='details']/p")[0].text_content(),
            "id": item.xpath(".//span[@class='courseId']")[0].text[:7],
        })
    return messages


def profile_image(response):
    return __parse_html(response).xpath("//a[@id='profileLink']/img/@src")[0]


def __survey_courses(response):
    import re, json
    return json.loads(re.search("json_ecb = ({.*?});", response).group(1))
