from . import Emails, Updates, Terms, Grades
from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from threading import Thread
from datetime import datetime
# Calculate term of "201710" format
this = datetime.today()
term = str(this.year) + (
    # Spring: 1st to 5th month, Summer: 6th to 7th and Fall: 8th to 12th
    "10" if this.month > 7 else "20" if this.month < 6 else "30"
)


# A class to add new items to data
class Add:
    # Date format e.g. "2017-12-31T23:59:59"
    date_format = "%Y-%m-%dT%H:%M:%S"

    # Class constructor that sets request and timestamp
    def __init__(self, request, date):
        self.request = request
        self.timestamp = self.get_timestamp(date)

    # Converts date string to timestamp (int)
    def get_timestamp(self, date):
        return datetime.strptime(date, self.date_format).timestamp()

    # Returns new items by comparing every item's time to the timestamp
    def get_new_items(self, items):
        return [item for item in items if self.get_timestamp(item["time"]) > self.timestamp]

    # Adds new items from API calls which returns a list of items
    def new_list(self, dictionary, query, api, args):
        dictionary[query] = self.get_new_items(api(self.request, *args).data)

    # Adds new items from API calls which returns a dictionary of items lists
    def new_dict(self, dictionary, queries, api, args):
        response = api(self.request, *args).data
        dictionary.update({query: self.get_new_items(response[query]) for query in queries})
