from datetime import datetime as __datetime
from os import path as __path
import re as __regex

# Regex for selecting English letters and cleaning numbers
__english = __regex.compile("[^\w /&.]", __regex.ASCII)
__clean_end = __regex.compile("[0-9]+$")

# Calculate term of "201710" format
__this = __datetime.today()
term_code = str(__this.year) + (
    # Spring: 1st to 5th month, Summer: 6th to 7th and Fall: 8th to 12th
    "10" if __this.month > 7 else "20" if __this.month < 6 else "30"
)


# Cleans course name
def clean_course_name(name):
    # From non English letters and from section numbers at the end
    return __clean_end.sub("", __english.sub("", name).strip()).strip()


# Gets a cache file path
def get_path(file):
    # Return a path of the file in Requests package's cache folder
    return __path.join(__path.dirname(__file__), "__pycache__/" + file + ".txt")
