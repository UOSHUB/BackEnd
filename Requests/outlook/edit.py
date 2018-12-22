from .values import __root_url, __email
import requests


# Sends an simple email from a user to another
def send_email(sid, pin, subject, body, recipients, save=True):
    # "recipients" has to be an array of strings
    if isinstance(recipients, str):
        # So if it's a string, put it in an array
        recipients = [recipients]
    # HTTP post request
    return requests.post(
        # To outlook-api/sendmail
        __root_url + "sendmail",
        # Basic authentication using sid(@sharjah.ac.ae) & pin
        auth=(__email(sid), pin),
        # JSON object containing sent email data
        json={
            # Email content and recipients
            "Message": {
                # Email Title
                "Subject": subject,
                # Email text body
                "Body": {
                    "ContentType": "HTML",
                    "Content": body
                },
                # Loop through and add recipients of the email
                "ToRecipients": [
                    {"EmailAddress": {"Address": recipient}} for recipient in recipients
                ]
                # Whether to show email in "Sent Items" page or not
            }, "SaveToSentItems": save
        }
        # Return the response status
    ).status_code


# Deletes an email (but keeps it in trash)
def delete_email(sid, pin, message_id):
    # Request to send email to trash
    return requests.post(
        # Using outlook-api/messages/<message id>/move
        __root_url + "messages/" + message_id + "/move",
        # Basic authentication using sid(@sharjah.ac.ae) & pin
        auth=(__email(sid), pin),
        # Move email to Deleted Items folder
        json={"DestinationId": "DeletedItems"}
        # Return the response status
    ).status_code


# Sends a email announcement about subscription and grades so far
def send_grades_summary(sid, courses, gpa, new_grade=None):
    # Store grade article as "an" for (A, F) or "a" for other grades
    if new_grade:
        grade, course = new_grade
        article = "an" if grade == "A" or grade == "F" else "a"
    return send_email(
        # Sender is me :)
        "u14111378", "74665403",
        # Email subject contains new grade or first subscription message
        f"You got {article} {grade} in {course}" if new_grade else "Subscribed to UOS HUB!",
        # Email body contains grades, GPA details, new grade or thanks for subscription message
        "<br>".join(([
            f"This is to inform you that you got {article} <b>{grade}</b> in <b>{course}</b><br>",
            "<i>Grades Checker was down today, it's up again now; sorry for the delayed notification.</i><br><br><br><hr>"
            "Here's a summary of your grades including this ☝ one and your GPA:<br>"
        ] if new_grade else [
            "Thank you for subscribing to UOS HUB Grades Checker,",
            "You'll get another email whenever a new grade comes out.<br><br><hr>"
            "For now, here's a summary for what's already out:<br>"
        ]) + ([
            "<b>Term grades so far:</b>",
            *[f"{course[1]}: {course[2]}" for course in sorted(courses, key=lambda course: len(course[1]))],
            f"<br><b>Term GPA so far</b>: {gpa['term']:.2f}",
            f"Cumulative GPA without this term was: {gpa['old']:.2f}",
            f"Cumulative GPA with this term so far is: <b>{gpa['new']:.2f}</b>"
        ] if courses else [
            "None of this term's grades have come out yet.",
            f"Your Cumulative GPA without this term is: {gpa['old']:.2f}"
        ]) + ["<br><br><hr>This is an automated notification from UOS HUB."]),
        # Recipient is the student
        __email(sid)
    )
