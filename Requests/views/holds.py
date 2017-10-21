from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import myudc


# Holds requests handler
class Holds(APIView):
    """
    This returns student's holds,
    which's an array of holds' data.
    """
    # Returns student's array of holds on GET request
    @login_required("myudc")
    def get(self, request):
        # Return an array of holds
        return Response(
            # Get & scrape holds data from MyUDC
            myudc.scrape.holds(
                myudc.get.holds(
                    # Send MyUDC session
                    request.session["myudc"],
                )
            )
        )
