from requests import post as __login
from .get import __root_url as root_url
from . import get, scrape


# Logs in myUDC and returns the session
def login(sid, pin):
    return __login(
        # Post data to login url
        root_url + "twbkwbis.P_ValLogin",
        # Send student id and password
        data={"sid": sid, "PIN": pin},
        # Required cookie for myUDC login
        cookies={"TESTID": "set"}
    ).cookies.get_dict()
