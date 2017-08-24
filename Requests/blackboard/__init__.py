# Formats an item in Blackboard id format
def __id(item):
    return "_{}_1".format(item)

# Root URL of UOS Blackboard
root_url = "https://elearning.sharjah.ac.ae/"


# Import hidden login function as top level
from .get import __login as login
# Import package modules to form its structure
from . import get, scrape, api, mobile
