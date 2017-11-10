from .general import root_url
# This file contains possible values of Blackboard variables

__lists = {
    "Announcements": 1,
    "Courses": 4,
    "Organizations": 5,
    "Tasks": 7,
    "Notes": 12,
    "Grades": 20,
    "Collages": 28,
    "Surveys": 257
}

__types = {
    "GB": "Item",
    "AS": "Assignment",
    "TE": "Assignment",
    "CR": "Course",
    "SU": "Survey",
    "CO": "Content",
    "AN": "Announcement",
}

__events = {
    "AVAIL": "Available",
    "OVERDUE": "Overdue",
    "DUE": "Due",
}

__terms = {
    "10": {
        "name": "FALL",
        "range": [12, 8]
    },
    "30": {
        "name": "SUM",
        "range": [7, 6]
    },
    "20": {
        "name": "SPR",
        "range": [5, 1]
    },
    "FALL": {
        "name": "Fall",
        "code": "10"
    },
    "SPR": {
        "name": "Spring",
        "code": "20"
    },
    "SUM": {
        "name": "Summer",
        "code": "30"
    },
}

# Store Blackboard stream urls
__stream_root_url = root_url + "webapps/streamViewer/"
__stream_url = __stream_root_url + "streamViewer"
__dismiss_update_url = __stream_root_url + "dwr_open/call/plaincall/NautilusViewService.removeRecipient.dwr"
