import requests


def get_emails(sid, pin, count, offset=0):
    return requests.get(
        "https://outlook.office365.com/api/v1.0/me/messages",
        auth=(sid + "@sharjah.ac.ae", pin),
        params={"$top": count, "$skip": offset}
    ).text


def send_email(sid, pin, subject, body, recipients):
    if isinstance(recipients, str):
        recipients = [recipients]
    return requests.post(
        "https://outlook.office365.com/api/v1.0/me/sendmail",
        auth=(sid + "@sharjah.ac.ae", pin),
        json={
            "Message": {
                "Subject": subject,
                "Body": {
                    "ContentType": "Text",
                    "Content": body
                },
                "ToRecipients": [
                    {"EmailAddress": {"Address": recipient + "@sharjah.ac.ae"}} for recipient in recipients
                ]
            }, "SaveToSentItems": "true"
        }
    ).status_code
