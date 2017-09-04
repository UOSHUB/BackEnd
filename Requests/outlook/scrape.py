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
