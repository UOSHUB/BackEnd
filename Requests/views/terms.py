from .common import login_required, client_side
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests import myudc


# Student's terms requests handler
class Terms(APIView):
    """
    This returns student's term details,
    which's a dictionary of courses' data.
    """
    server = "myudc"

    # Returns term dictionary of requested term on GET request
    @login_required
    def get(self, request, term=None):
        # If accessing "/terms/" without specifying term
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
        # Return student's term details
        return Response(
            # Get & scrape student's term from myUDC
            myudc.scrape.term(
                myudc.get.term(
                    # Send term code & myUDC cookies
                    term, request.session["myudc"]
                )
            )
        )
