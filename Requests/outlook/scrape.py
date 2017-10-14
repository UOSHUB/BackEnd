from Requests import clean_course_name as __clean
import re

# Regex expression to extract required details from generated emails
__content = re.compile("(.+): (?P<title>.+) has been added to course: (?P<course>.+)\. Click")
__assignment = re.compile("Assignment: (?P<title>.+) in course: (?P<course>.+) is due: .+, (.{3}).* ([0-9]+),")
__announcement = re.compile("(?:New Announcement Available in course )?(?P<course>.+?): (?P<title>.+)")
__clean_event = re.compile("^(?:New Announcement: |إعلان جديد :)")


# Scrapes basic info about emails for preview purposes
def emails_previews(emails):
    # Array to store email previews
    previews = []
    # Loop through emails
    for email in emails:
        # If email isn't about a Blackboard content item being added
        if not email["BodyPreview"].startswith("Content Item"):
            # Assume email subject is in this format "event: title"
            subject = email["Subject"].split(":", 1)
            event = subject[0]
            # Consider email personal if there's no event
            if len(subject) == 1:
                event = "Personal"
            # If email event is shortened to "re", make it "Reply"
            elif event.lower().startswith("re"):
                event = "Reply"
            # Add preview email data to previews
            previews.append({
                # Title is the last part of subject
                "title": subject[-1].strip(),
                "event": event,
                # Get email time & sender directly
                "time": email["DateTimeSent"],
                "sender": email["Sender"]["EmailAddress"]["Name"]
            })
    return previews


# Scrapes Blackboard generated courses emails
def courses_emails(raw_emails):
    # Array to store emails
    emails = []
    # Loop through raw emails
    for email in raw_emails:
        # Store email preview and subject
        preview = email["BodyPreview"]
        subject = email["Subject"]
        # Match content details and format email event
        # When email is about an assignment due
        if subject.startswith("Assignment:"):
            match = __assignment.match(subject)
            event = "Assignment Due " + match.group(3) + " " + match.group(4)
        # When email is about an assignment or content item being added
        elif preview.startswith("Content Item:") or preview.startswith("Assignment:"):
            match = __content.match(preview)
            event = "New {}".format(match.group(1).split()[0])
        else:  # When email is about an announcement
            match = __announcement.match(subject)
            event = "New Announcement"
        # Add extracted email data to emails
        emails.append({
            "event": event,
            # Extract title and course using Regex matches
            "title": match.group("title"),
            "course": __clean(match.group("course")),
            # Get email time and body directly
            "time": email["DateTimeSent"],
            "body": email["Body"]["Content"]
        })
    return emails


# Scrapes university events related emails
def events_emails(raw_emails):
    # Return an array of emails dictionaries
    return [
        {   # Extract and add event body, time and cleaned title
            "title": __clean_event.sub("", email["Subject"]),
            "time": email["DateTimeSent"],
            "body": email["Body"]["Content"]
        }   # Loop through raw emails
        for email in raw_emails
    ]
