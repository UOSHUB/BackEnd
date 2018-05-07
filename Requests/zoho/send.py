from Requests.outlook.values import __email
import os, requests

# Get token from environment and store it in dictionary
auth = {"Authorization": os.environ.get("TOKEN")}

# Get account URL from environment and store it
url = os.environ.get("ACCOUNT")


# General function to send an email using Zoho API
def email(sender, recipient, subject, body):
    # Post a request with token in the header and return status
    return requests.post(url, headers=auth, json={
        # Specify sender and recipient
        "fromAddress": sender,
        "toAddress": recipient,
        # Specify email subject and body
        "subject": subject,
        "content": body
    }).status_code


# Sends a email announcement about a grade of a course
def grade_announcement(sid, course, grade):
    # Store grade article as "an" for (A, F) or "a" for other grades
    article = "an" if grade == "A" or grade == "F" else "a"
    # Send the email
    return email(
        # Sender is UOS HUB NO-REPLY
        "UOS HUB <no-reply@uoshub.com>",
        # Recipient is the student
        __email(sid),
        # Email subject and body details the grade and the course
        "You got " + article + " " + grade + " in " + course,
        "This is an automated notification from uoshub.com<br><br>" +
        "It is to inform you that you got " + article + " <b>" + grade + "</b> in <b>" + course + "</b>"
    )
