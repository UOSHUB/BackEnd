import requests

# Commonly used outlook api link and email domain name
root_url = "https://outlook.office365.com/api/v1.0/me/"
email = "{}@sharjah.ac.ae"


# Login to outlook
def login(sid, pin):
    # HTTP get request from api root with basic authentication that returns success or failure
    return requests.get(root_url, auth=(email.format(sid), pin)).status_code == 200


# Gets the latest emails of a user
def get_emails(sid, pin, count=25, offset=0):
    # HTTP get request
    return requests.get(
        # From outlook-api/messages
        root_url + "messages",
        # Basic authentication using sid(@sharjah.ac.ae) & pin
        auth=(email.format(sid), pin),
        # '$top': number of requested emails, '$skip': number of skipped emails
        params={"$top": count, "$skip": offset}
    ).text


# Sends an simple email from a user to another
def send_email(sid, pin, subject, body, recipients):
    # 'recipients' has to be an array of strings
    if isinstance(recipients, str):
        # So if it's a string, put it in an array
        recipients = [recipients]
    # HTTP post request
    return requests.post(
        # To outlook-api/sendmail
        root_url + "sendmail",
        # Basic authentication using sid(@sharjah.ac.ae) & pin
        auth=(email.format(sid), pin),
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
                    {"EmailAddress": {"Address": email.format(recipient)}} for recipient in recipients
                ]
                # Whether to show email in "Sent Items" page or not
            }, "SaveToSentItems": "true"
        }
        # Return the response status
    ).status_code
