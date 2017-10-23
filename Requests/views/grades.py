from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import blackboard


# Grades requests handler
class Grades(APIView):
    """
    This returns student's Blackboard grades,
    which's an array of grades' details.
    """
    # Returns student's array of grades on GET request
    @login_required("blackboard")
    def get(self, request, term):
        # If requesting grades API root path
        return Response({
            # Return a dictionary of {term name: url of grades in term} pairs
            term_name: request.build_absolute_uri(term_code + "/")
            # Get & scrape then loop through available terms in Blackboard
            for term_name, term_code in blackboard.scrape.terms_list(
                blackboard.get.courses_list(
                    request.session["blackboard"]
                )
            ).items()
        })
