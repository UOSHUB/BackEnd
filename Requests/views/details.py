from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import blackboard


# Website's layout details requests handler
class LayoutDetails(APIView):
    """
    This only returns student's basic info right now,
    but in the future it will have all layout details including:
    theme preferences, student's modifications and other settings
    """
    # Returns layout details on GET request
    @staticmethod
    @login_required("blackboard")
    def get(request):
        # Return student's basic info as of now
        return Response({
            # Get student's basic info from Blackboard
            "student": blackboard.get.basic_info(
                # Send Blackboard cookies
                request.session["blackboard"],
                # And current student id
                request.session["sid"]
            )
        })
