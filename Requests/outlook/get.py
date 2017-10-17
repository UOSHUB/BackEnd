from .values import root_url, email, __search_queries
import requests


# General Outlook emails GET request with common attributes
def api(sid, pin, params, sub_url=""):
    # HTTP GET request to Outlook API
    return requests.get(
        # From outlook-api/messages/<sub_url>
        root_url + "messages/" + sub_url,
        # Basic authentication using sid(@sharjah.ac.ae) & pin
        auth=(email.format(sid), pin),
        # Send all necessary request parameters
        params=params
        # Return data in JSON format
    ).json()["value"]


# Gets the latest emails of a user
def emails(sid, pin, count=25, offset=0, search=None):
    # Request from API using credentials and parameters
    return api(sid, pin, dict(
        {   # $top: number of requested emails
            "$top": count,
            # $select: returns selected fields only (required ones)
            "$select": "DateTimeSent,Subject,BodyPreview,Sender"
        }, **(  # If a search query is required, send it in the request. Otherwise $skip: number of skipped emails
            {"$search": "\"{}\"".format(__search_queries[search])} if search else {"$skip": offset}
        )
    ))

