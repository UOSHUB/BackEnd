from .get import url
import requests

# Append Blackboard Mobile path to website URL
url += "Bb-mobile-bb_bb60/"


# Logs in Blackboard Mobile and returns the session
def login(sid, pin):
    # Post HTTP request and store its response
    response = requests.post(
        # Post data to login url
        url + 'sslUserLogin',
        # Send student id and password
        data={'username': sid, 'password': pin}
    )
    # If response status is not 'OK'
    if 'OK' not in response.text:
        # Raise an error to indicate login failure
        raise ConnectionError("Wrong Credentials!")
    # If login succeeded, send back session cookies
    return response.cookies.get_dict()
