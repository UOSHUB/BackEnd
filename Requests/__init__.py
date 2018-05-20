from datetime import datetime as __datetime
import re as __regex

# Semesters (code, name) pairs
seasons_codes = {
    "10": "Fall Semester",
    "20": "Spring Semester",
    "30": "Summer Session",
    "Fall": "10",
    "Spring": "20",
    "Summer": "30"
}

# Regex for selecting English letters and cleaning numbers
__english = __regex.compile("[^\w /&.]", __regex.ASCII)
__clean_end = __regex.compile("[0-9]+$")

# Compute term of "201710" format
__this = __datetime.today()
# If it's spring or summer semester, deduct one year to match academic year
term_code = str(__this.year - (1 if __this.month < 8 else 0)) + seasons_codes[
    # Spring: 1st to 5th month, Summer: 6th to 7th and Fall: 8th to 12th
    "Fall" if __this.month > 7 else "Spring" if __this.month < 6 else "Summer"
]


# Cleans course name
def clean_course_name(name):
    # From non English letters and from section numbers at the end
    return __clean_end.sub("", __english.sub("", name).strip()).strip()
