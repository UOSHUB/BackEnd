from .values import __root_url, __email, __file, __search_queries
from base64 import b64decode
import requests


# General Outlook emails GET request with common attributes
def api(sid, pin, params, sub_url=""):
    # HTTP GET request to Outlook API
    return requests.get(
        # From outlook-api/messages/<sub_url>
        __root_url + "messages/" + sub_url,
        # Basic authentication using sid(@sharjah.ac.ae) & pin
        auth=(__email.format(sid), pin),
        # Send all necessary request parameters
        params=params
        # Return data in JSON format
    ).json()


# Gets the latest emails of a user
def emails_list(sid, pin, count=25, offset=0, search=None):
    # Request from API using credentials and parameters
    return api(sid, pin, dict(
        {   # $top: number of requested emails
            "$top": count,
            # $select: returns selected fields only (required ones)
            "$select": "DateTimeReceived,Subject,BodyPreview,Sender"
        }, **(  # If a search query is required, send it in the request. Otherwise $skip: number of skipped emails
            {"$search": "\"{}\"".format(__search_queries[search])} if search else {"$skip": offset}
        )
    ))["value"]


# Gets a single email's body and its images
def email_body(sid, pin, message_id):
    # Request email HTML body using credentials and message id
    message = api(sid, pin, {"$select": "Body"}, message_id)
    # If message contains images
    if "cid:" in message["Body"]["Content"]:
        # Request email attachments and append it to message
        message["Attachments"] = api(sid, pin, {
            # Only get attachments' content ids
            "$select": __file + "ContentId"
        }, message_id + "/attachments")["value"]
    return message


# Gets a single email's attachment after decoding it
def email_attachment(sid, pin, message_id, attachment_id):
    # Request email attachment using credentials
    attachment = api(sid, pin, {
        # Only get the attachment itself and its type
        "$select": __file + "ContentBytes,ContentType"
        # Specify message id and attachment id
    }, message_id + "/attachments/" + attachment_id)
    # Return attachment encoded bytes and type
    return {
        "content": b64decode(attachment["ContentBytes"].encode()),
        "content_type": attachment["ContentType"]
    }
