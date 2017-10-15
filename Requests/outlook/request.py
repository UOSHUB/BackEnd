from .values import root_url, email, __search_queries
import requests


# Login to outlook
def login(sid, pin):
    # HTTP get request from api root with basic authentication that returns success or failure
    return requests.get(root_url, auth=(email.format(sid), pin)).status_code == 200


# Gets the latest emails of a user
def get_emails(sid, pin, count=25, offset=0, search=None):
    # HTTP get request
    return requests.get(
        # From outlook-api/messages
        root_url + "messages",
        # Basic authentication using sid(@sharjah.ac.ae) & pin
        auth=(email.format(sid), pin),
        # Send all necessary request parameters
        params=dict({
            # $top: number of requested emails
            "$top": count,
            # $select: returns selected fields only (required ones)
            "$select": "DateTimeSent,Subject,BodyPreview,Body" + ("" if search in ["Events", "Courses"] else ",Sender")
        }, **(  # If a search query is required, send it in the request. Otherwise $skip: number of skipped emails
            {"$search": "\"{}\"".format(__search_queries[search])} if search else {"$skip": offset}
        ))
    ).json()["value"]


# Sends an simple email from a user to another
def send_email(sid, pin, subject, body, recipients):
    # "recipients" has to be an array of strings
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
