from .values import __root_url, __email
import requests


# Sends an simple email from a user to another
def send_email(sid, pin, subject, body, recipients):
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
                    "ContentType": "Text",
                    "Content": body
                },
                # Loop through and add recipients of the email
                "ToRecipients": [
                    {"EmailAddress": {"Address": recipient}} for recipient in recipients
                ]
                # Whether to show email in "Sent Items" page or not
            }, "SaveToSentItems": "true"
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
