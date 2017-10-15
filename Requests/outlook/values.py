import re

# Commonly used outlook api link and email domain name
root_url = "https://outlook.office365.com/api/v1.0/me/"
email = "{}@sharjah.ac.ae"

# Emails categories search queries
__search_queries = {
    # Search for university announcements/events emails
    "events": "from:no-reply@sharjah.ac.ae",
    # Search Blackboard generated notifications about courses related events
    "courses": "from:do-not-reply@sharjah.uos.edu",
    # Search for everything else, which we consider as personal emails
    "personal": "NOT from:do-not-reply@sharjah.uos.edu AND NOT from:no-reply@sharjah.ac.ae"
}

# Dictionary & Regex to extract "Reply" & "Forward" emails
__events = {"re": "Reply", "fw": "Forward"}
__split_subject = re.compile("^(?:(re|fw|fwd): )?(.*)$", re.IGNORECASE)

# Regex expression to extract required details from generated emails
__content = re.compile("(.+): (?P<title>.+) has been added to course: (?P<course>.+)\. Click")
__assignment = re.compile("Assignment: (?P<title>.+) in course: (?P<course>.+) is due: .+, (.{3}).* ([0-9]+),")
__announcement = re.compile("(?:New Announcement Available in course )?(?P<course>.+?): (?P<title>.+)")
__clean_event = re.compile("^(?:New Announcement: |إعلان جديد :)")
