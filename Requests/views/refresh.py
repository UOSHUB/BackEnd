from . import Emails, Updates, Terms, Grades
from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from threading import Thread
from datetime import datetime

# Calculate term of "201710" format
this = datetime.today()
term_code = str(this.year) + (
    # Spring: 1st to 5th month, Summer: 6th to 7th and Fall: 8th to 12th
    "10" if this.month > 7 else "20" if this.month < 6 else "30"
)


# Refreshing data requests handler
class Refresh(APIView):
    """
    This returns a dictionary of lists containing
    items that are newer than the sent date (timestamp)
    they can be from any of the other API calls
    """
    # Returns items newer than the sent date on GET request
    @staticmethod
    @login_required("myudc")
    @login_required("blackboard")
    def get(request, date):
        # Notify if no date is specified
        if not date:
            return Response("You didn't specify a date (timestamp)")
        # Declare required variables
        data, threads = {}, []
        add = Add(request, date)
        queries = request.query_params

        # Shortens creating & starting a thread
        def start(target, *args):
            thread = Thread(target=target, args=args)
            threads.append(thread)
            thread.start()
        # If querying emails
        if "emails" in queries:
            data["emails"] = {}
            # Loop through requested category(s) if any. Otherwise, loop through all of them
            for category in queries["emails"].split(",") if queries["emails"] else ["personal", "courses", "events"]:
                # Start a thread to grab the new items of each category
                start(add.new_list, data["emails"], category, Emails.get, [category, 10])
        # If querying content
        if "content" in queries:
            content = queries["content"]
            # If content type is not specified
            if not content:
                # Start a thread to grab new documents and deadlines
                start(add.new_dict, data, Terms.Content.get, [term_code, "content"])
            # If it is either documents or deadlines
            elif content in ["documents", "deadlines"]:
                # Start a thread to grab new items in specified content type
                start(add.new_list, data, content, Terms.Content.get, [term_code, content])
        # If querying updates
        if "updates" in queries:
            # Start a thread to grab new updates
            start(add.new_list, data, "updates", Updates.get, [])
        # If querying grades
        if "grades" in queries:
            # Start a thread to grab new grades
            start(add.new_list, data, "grades", Grades.get, [term_code])
        # Loop through threads and join them to the main thread
        [thread.join() for thread in threads]
        return Response(data)


# A class to add new items to data
class Add:
    # General date format e.g. "2017-12-31T23:59:59+0400"
    date_format = "%Y-%m-%dT%H:%M:%S%z"

    # Class constructor that sets request and timestamp
    def __init__(self, request, date):
        self.request = request
        self.timestamp = self.get_timestamp(date + "+0400")

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
    def new_dict(self, dictionary, api, args):
        for query, items in api(self.request, *args).data.items():
            dictionary[query] = self.get_new_items(items)
