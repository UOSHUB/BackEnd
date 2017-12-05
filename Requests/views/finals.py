from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import myudc
from .terms import Terms
from time import time


# Final Exams requests handler
class Finals(APIView):
    """
    This returns student's final exams schedule,
    which's an array of final exams' data.
    """
    # Returns student's array of final exams on GET request
    @staticmethod
    @login_required("myudc")
    def get(request, term_code):
        # Return all available terms if non is specified
        if not term_code:
            return Terms.get(request)
        # Reset MyUDC time to force login on the next request
        request.session["myudc_time"] = time() - 15*60
        # Return an array of finals exams
        return Response(
            # Get & scrape final exams data from MyUDC
            myudc.scrape.final_exams(
                myudc.get.final_exams(
                    # Send MyUDC session
                    request.session["myudc"],
                    # Send term code
                    term_code
                )
            )
        )
