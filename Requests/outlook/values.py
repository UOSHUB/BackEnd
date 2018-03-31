import re


# Formats student id into email address
def __email(sid):
    return f"{sid}@sharjah.ac.ae"


# Commonly used outlook api link
__root_url = "https://outlook.office365.com/api/v1.0/me/"
__file = "Microsoft.OutlookServices.FileAttachment/"
# Form a string of blocked emails in the personal category
__black_list = " OR ".join([
    __email(sender) for sender in [
        "no-reply", "Library", "register", "ITC", "uos-Admission", "chancellor-office"
    ]
])

# Emails categories search queries
__search_queries = {
    # Search for university announcements/events emails
    "events": f"from:({__black_list})",
    # Search Blackboard generated notifications about courses related events
    "courses": "from:do-not-reply@elearning.sharjah.ac.ae",
    # Search for everything else, which we consider as personal emails
    "personal": f"NOT from:(do-not-reply@elearning.sharjah.ac.ae OR {__black_list})"
}

# Dictionary & Regex to extract "Reply" & "Forward" emails
__events = {"re": "Reply", "fw": "Forward"}
__split_subject = re.compile("^(?:(re|fw|fwd): )?(.*)$", re.IGNORECASE)

# Regex expression to extract required details from generated emails
__content = re.compile("(.+): (?P<title>.+) has been added to course: (?P<course>.+)\. Click")
__assignment = re.compile("Assignment: (?P<title>.+) in course: (?P<course>.+) is due: .+, (.{3}).* ([0-9]+),")
__announcement = re.compile("(?:New Announcement Available in course )?(?P<course>.+?): (?P<title>.+)")
__clean_event = re.compile("^(?:New Announcement: |إعلان جديد :)")
