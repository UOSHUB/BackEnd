from Requests.outlook.values import __email
import os, requests

# Get token from environment and store it in dictionary
auth = {"Authorization": os.getenv("TOKEN")}

# Get account URL from environment and store it
url = os.getenv("ACCOUNT")


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

