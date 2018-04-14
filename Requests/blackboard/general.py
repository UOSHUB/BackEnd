import requests
# Root and sub URLs of UOS Blackboard
root_url = "https://elearning.sharjah.ac.ae/"
__web = root_url + "webapps/"
__api = root_url + "learn/api/public/v1/"
__mobile = root_url + "webapps/Bb-mobile-bb_bb60/"
__documents = root_url + "bbcswebdav/pid-{0}-dt-content-rid-{1}_1/xid-{1}_1"


# Formats an item in Blackboard id format
def __id(item):
    return f"_{item}_1"


# Logs in Blackboard Mobile and returns the session
def login(sid, pin):
    # Post HTTP request and store its response
    response = requests.post(
        # Post data to login url
        __mobile + "sslUserLogin",
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
        __web + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).text


# General Blackboard Mobile request with common attributes
def mobile(link, session, params=None):
    return requests.get(
        # Get data from mobile url + sub-url
        __mobile + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).content


# General Blackboard API request with common attributes
def api(link, session, params=None):
    return requests.get(
        # Get data from api url + api sub-url
        __api + link,
        # Send login session
        cookies=session,
        # Send required data
        params=params
    ).json()
