from .common import login_required, client_side
from rest_framework.response import Response
from rest_framework.views import APIView
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
    def get(request, update_id=None):
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

    # Deletes an update if specified, otherwise deletes all updates
    @staticmethod
    @login_required("blackboard")
    def delete(request, update_id):
        # Loop through all updates or a single update if specified
        for update in [{"dismiss": update_id}] if update_id else Updates.get(request).data:
            # Request a Blackboard edit to dismiss the update
            blackboard.edit.dismiss_update(
                # Send Blackboard cookies and update id
                request.session["blackboard"], update["dismiss"]
            )
        # Return successful response. But on browser, return updated list
        return Response() if client_side(request) else Updates.get(request)
