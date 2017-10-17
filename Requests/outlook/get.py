from .values import root_url, email, __search_queries
import requests


# Gets the latest emails of a user
def emails(sid, pin, count=25, offset=0, search=None):
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

