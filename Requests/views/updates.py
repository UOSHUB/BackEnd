from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import blackboard


# Student's updates requests handler
class Updates(APIView):
    server = "blackboard"
    """
    This returns student's Blackboard updates,
    which is a dictionary of updates and the
    names of the courses they are coming from.
    """
    # Returns updates dictionary of all courses on GET request
    @login_required
    def get(self, request):
        # Return updates object
        return Response(
            # Get & scrape student's updates from Blackboard
            blackboard.scrape.updates(
                blackboard.get.updates(
                    # Send Blackboard cookies
                    request.session["blackboard"]
                )
            )
        )
