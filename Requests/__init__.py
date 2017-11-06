import re as __regex

# Regex for selecting English letters and cleaning numbers
__english = __regex.compile("[^\w /&.]", __regex.ASCII)
__clean_end = __regex.compile("[0-9]+$")


# Cleans course name
def clean_course_name(name):
    # From non English letters and from section numbers at the end
    return __clean_end.sub("", __english.sub("", name).strip()).strip()

