from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import blackboard
from threading import Thread


# Student's updates requests handler
class Updates(APIView):
    """
    This returns student's Blackboard updates,
    which is a dictionary of updates indexed
    by the courses they came from.
    """
    # Returns updates dictionary of all courses on GET request
    @staticmethod
    @login_required("blackboard")
    def get(request):
        # Store Blackboard cookies and empty dictionaries
        cookies = request.session["blackboard"]
        updates, courses = [], {}
        # Instantiate a thread that gets courses dictionary
        courses_thread = Thread(target=lambda: courses.update(
            # Get & scrape courses dictionary from Blackboard
            blackboard.scrape.courses_dictionary(
                blackboard.get.courses_list(cookies)
            )
        ))
        # Instantiate a thread that gets raw updates object
        updates_thread = Thread(target=lambda: updates.extend(
            # Get student's updates object from Blackboard
            blackboard.get.updates(cookies)
        ))
        # Start executing threads
        courses_thread.start()
        updates_thread.start()
        # Then join them with main thread
        courses_thread.join()
        updates_thread.join()
        # Return updates dictionary
        return Response(
            # Get & scrape student's updates from Blackboard
            blackboard.scrape.updates(
                # Send updates and courses
                updates, courses
            )
        )
