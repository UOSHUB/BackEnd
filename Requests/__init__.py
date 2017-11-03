import re as __regex

# General date format e.g. "2017-12-31T23:59:59"
date_format = "%Y-%m-%dT%H:%M:%S"

# Regex for selecting English letters and cleaning numbers
__english = __regex.compile("[^\w /&.]", __regex.ASCII)
__clean_end = __regex.compile("[0-9]+$")


# Cleans course name
def clean_course_name(name):
    # From non English letters and from section numbers at the end
    return __clean_end.sub("", __english.sub("", name).strip()).strip()

