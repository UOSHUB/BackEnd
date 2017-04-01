from mechanize import Browser as Mechanize, _http, LinkNotFoundError, ControlNotFoundError, URLError
from bs4 import BeautifulSoup
import ssl


# A mechanize subclass with frequently use methods
class Browser(Mechanize):
    def __init__(self):
        # Instantiate superclass mechanize browser
        Mechanize.__init__(self)
        # Browser options
        self.set_handle_equiv(True)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_robots(False)
        self.set_handle_refresh(_http.HTTPRefreshProcessor(), max_time=1)
        # Disable SSL verification in Python
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
        except AttributeError: pass

    # Gets UOS UDC link by providing sub url only
    def get(self, sub_url):
        try:
            self.open('https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_' + sub_url)
        # Try again if opening the link fails
        except URLError:
            self.get(sub_url)

    # Follows a UOS UDC link by providing sub link only
    def follow(self, sub_link):
        try:
            self.follow_link(url='/prod_enUS/' + sub_link)
        # Try again if following the link fails
        except URLError:
            self.follow(sub_link)
        # Return false if link isn't found
        except LinkNotFoundError:
            return False
        # Otherwise return true
        else:
            return True

    # Returns BeautifulSoup object of current page
    def get_soup(self):
        return BeautifulSoup(self.response().read(), 'lxml')

    # Login to official UOS UDC
    def login(self, sid, pin):
        # Open original UOS UDC login url
        self.get('WWWLogin')
        # Fill up login form
        self.select_form(nr=0)
        try:
            self['sid'] = str(sid)
            self['PIN'] = str(pin)
        except ControlNotFoundError:
            return self.login(sid, pin)
        # Submit and return login validation
        self.submit()
        return self.title() == 'Main Menu'

    # Returns student's first name
    def get_username(self):
        # Enter Personal Information section
        self.get('GenMenu?name=bmenu.P_GenMnu')
        # Enter Directory Profile page
        self.follow('bwgkoprf.P_ShowDiroItems')
        # Extract and return student name from soup
        return self.get_soup().find('td', class_='dedefault').string.split()[0]

# Instantiate a scraper object to be used
# in many different places (statically, kind of)
br = Browser()
