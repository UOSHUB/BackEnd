from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import myudc


# Student's details requests handler
class Student(APIView):
    """
    This only returns student's basic info right now,
    but in the future it will have all layout details including:
    theme preferences, student's modifications and other settings
    """
    # Returns student's details on GET request
    @staticmethod
    @login_required("myudc")
    def get(request):
        # Return student's basic info as of now
        return Response(
            # Get & scrape student's basic info from MyUDC
            myudc.scrape.student_details(
                myudc.get.summarized_schedule(
                    # Send MyUDC cookies
                    request.session["myudc"]
                )
            )
        )
