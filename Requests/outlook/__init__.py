from .values import __root_url, __email
from requests import get as __login
from . import get, scrape, edit


# Login to outlook
def login(sid, pin):
    # HTTP get request from api root with basic authentication that returns success or failure
    return __login(__root_url, auth=(__email(sid), pin)).status_code == 200
