from .common import login_required, client_side
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests import myudc


# Student's schedule requests handler
class Schedule(APIView):
    server = "myudc"
    """
    This returns student's schedule details,
    which's a dictionary of courses that contain:
    course id, title, days, time, crn, location, etc..
    """
    # Returns schedule dictionary of requested term on GET request
    @login_required
    def get(self, request, term=None):
        # If accessing "/schedule" without specifying term
        if not term:
            # Get & scrape all registered terms
            terms = myudc.scrape.registered_terms(
                myudc.get.reg_history(
                    # Send myUDC cookies
                    request.session["myudc"]
                )
            )
            # Return all terms as {term code: term name} pairs
            return Response(terms if client_side(request) else {
                # Unless it's a browser, then make it {term name: term url} pairs
                name: request.build_absolute_uri(code) + "/"
                # By looping through all terms and formatting them
                for code, name in terms.items()
            })
        # Return student's schedule details
        return Response(
            # Get & scrape student's schedule from myUDC
            myudc.scrape.schedule(
                myudc.get.schedule(
                    # Send term code & myUDC cookies
                    term, request.session["myudc"]
                )
            )
        )