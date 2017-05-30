from lxml.html import fromstring as __parse_html
import re, json


def courses(response):
    return {link.text[:7]: link.attrib["href"][54:-7] for link in __parse_html(response).find(".//ul").findall(".//a")}


def survey_courses(response):
    return json.loads(re.search("json_ecb = ({.*?});", response).group(1))
