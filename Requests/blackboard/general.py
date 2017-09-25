import requests
# Root and sub URLs of UOS Blackboard
root_url = "https://elearning.sharjah.ac.ae/"
__web = "webapps/"
__mobile = __web + "Bb-mobile-bb_bb60/"


# Formats an item in Blackboard id format
def __id(item):
    return "_{}_1".format(item)


# Logs in Blackboard Mobile and returns the session
def login(sid, pin):
    # Post HTTP request and store its response
    response = requests.post(
        # Post data to login url
        root_url + __mobile + "sslUserLogin",
        # Send student id and password
        data={"username": sid, "password": pin}
    )
    # If response status is not "OK"
    if "status=\"OK\"" not in response.text:
        # Raise an error to indicate login failure
        raise ConnectionError("Wrong Credentials!")
    # If login succeeded, send back session cookies
    return response.cookies.get_dict()


# General Blackboard request to "webapps/" with common attributes
def web(link, session, params=None):
    return requests.get(
        # Get data from website url + sub-url
        root_url + __web + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).text


# General Blackboard Mobile request with common attributes
def mobile(link, session, params=None):
    return requests.get(
        # Get data from mobile url + sub-url
        root_url + __mobile + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).content


# General Blackboard API request with common attributes
def api(link, session, params=None):
    return requests.get(
        # Get data from api url + api sub-url
        root_url + "learn/api/public/v1/" + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).json()
