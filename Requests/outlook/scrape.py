from Requests import clean_course_name as __clean, date_format as __date_format
from re import sub as __replace
from .values import (
    __convert_date, __offset, __split_subject,
    __events, __assignment, __content,
    __announcement, __clean_event
)


# Returns common email details in a dictionary
def __common(email, sender, title):
    return dict({
        "sender": sender["Name"],
        "from": sender["Address"]
        # Add sender name & address if available
    } if sender else {},
        # Add email title, id and ISO formatted time
        title=title,
        id=email["Id"][-13:-1],
        time=(__convert_date(
            # Convert time string and add timezone offset
            email["DateTimeReceived"][:-1], __date_format
        ) + __offset).isoformat()
    )


# Scrapes personal emails details
def personal_emails(raw_emails):
    # Array to store emails
    emails = []
    # Loop through raw emails
    for email in raw_emails:
        # Match and store email event (if any), title and sender
        event, title = __split_subject.match(email["Subject"]).groups()
        # Add extracted email details to emails
        emails.append(dict(
            __common(email, email["Sender"]["EmailAddress"], title),
            # Extract event using Regex matches then add it
            event=__events[event[:2].lower()] if event else "New Email",
        ))
    return {
        "personal": emails,
        "idRoot": raw_emails[0]["Id"][:-14]
    }


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
        # Add extracted email details to emails
        emails.append(dict(
            __common(email, None, match.group("title")),
            # Add event and extract title using Regex matches
            event=event, course=__clean(match.group("course")),
        ))
    return {
        "courses": emails,
        "idRoot": raw_emails[0]["Id"][:-14]
    }


# Scrapes university events related emails
def events_emails(raw_emails):
    return {
        "events": [
            __common(  # Extract and add email's common fields
                email, email["Sender"]["EmailAddress"],
                __clean_event.sub("", email["Subject"])
            )  # Loop through raw emails
            for email in raw_emails
        ], "idRoot": raw_emails[0]["Id"][:-14]
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
            body = __replace(
                # Search for src="cid:<ContentId>"
                "src=\"cid:" + image["ContentId"] + "\"",
                # Replace it with src="data:<ContentType>;base64,<ContentBytes>"
                "src=\"data:" + image["ContentType"] + ";base64," + image["ContentBytes"] + "\"",
                # Do that in HTML body and only once
                body, 1
            )
    return body
