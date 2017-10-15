from rest_framework.response import Response
from rest_framework.views import APIView
from .common import client_side


# API root (/api/) requests handler
class APIRoot(APIView):
    """
    UOSHUB Restful API root URL.
    Notice that all API calls require login first except for calendar calls.
    """
    # Returns list of available API calls on GET request
    @staticmethod
    def get(request, invalid):
        # Store a URL builder relative to /api/
        url = lambda path: request.build_absolute_uri("/api/" + path)
        # Display a list of available API calls to browser or nothing if client
        return Response({} if client_side(request) else dict({
            "Login": url("login/"),
            "Layout Details": url("details/"),
            "Updates": url("updates/"),
            "Terms": url("terms/"),
            "Courses": url("courses/"),
            "Emails": url("emails/"),
            "Calendar": url("calendar/"),
            "Holds": url("holds/"),
        }, **(  # If requested path isn't a supported API call, add an error message to indicate it
            {"Error": [request.path + " isn't a supported API call"]} if invalid else {})
        ))
