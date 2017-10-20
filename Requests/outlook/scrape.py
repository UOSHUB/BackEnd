from .values import __split_subject, __events, __assignment, __content, __announcement, __clean_event
from Requests import clean_course_name as __clean
import re


# Scrapes personal emails details
def personal_emails(raw_emails):
    # Array to store emails
    emails = {}
    # Loop through raw emails
    for email in raw_emails:
        # Match and store email event (if any), title and sender
        event, title = __split_subject.match(email["Subject"]).groups()
        sender = email["Sender"]["EmailAddress"]
        # Add extracted email details to emails
        emails[email["Id"][-13:-1]] = {
            # Extract event and title using Regex matches
            "title": title,
            "event": __events[event[:2].lower()] if event else "New Email",
            # Get time, sender name and email
            "time": email["DateTimeSent"],
            "sender": sender["Name"],
            "from": sender["Address"]
        }
    return {
        "personal": emails,
        "idRoot": raw_emails[0]["Id"][:-14]
    }


# Scrapes Blackboard generated courses emails
def courses_emails(raw_emails):
    # Array to store emails
    emails = {}
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
        emails[email["Id"][-13:-1]] = {
            "event": event,
            # Extract title and course using Regex matches
            "title": match.group("title"),
            "course": __clean(match.group("course")),
            # Get email time directly
            "time": email["DateTimeSent"]
        }
    return {
        "courses": emails,
        "idRoot": raw_emails[0]["Id"][:-14]
    }


# Scrapes university events related emails
def events_emails(raw_emails):
    # Array to store emails
    emails = {}
    # Loop through raw emails
    for email in raw_emails:
        sender = email["Sender"]["EmailAddress"]
        # Extract and add event cleaned title, time, sender name and email
        emails[email["Id"][-13:-1]] = {
            "title": __clean_event.sub("", email["Subject"]),
            "time": email["DateTimeSent"],
            "sender": sender["Name"],
            "from": sender["Address"]
        }
    return {
        "events": emails,
        "idRoot": raw_emails[0]["Id"][:-14]
    }


# Scrapes a single email's body and embeds its images
def email_body(message):
    # Store email's HTML body
    body = message["Body"]["Content"]
    # If email has images attached
    if "Attachments" in message:
        # Loop through attached images
        for image in message["Attachments"]:
            # Use Regex to replace image id by its bytes
            body = re.sub(
                # Search for src="cid:<ContentId>"
                "src=\"cid:" + image["ContentId"] + "\"",
                # Replace it with src="data:<ContentType>;base64,<ContentBytes>"
                "src=\"data:" + image["ContentType"] + ";base64," + image["ContentBytes"] + "\"",
                # Do that in HTML body and only once
                body, 1
            )
    return body
