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
        # If client side is accessing an invalid path
        if client_side(request) and invalid:
            # Return an error message with NOT_FOUND status
            return Response("API path not found!", status=404)
        # Otherwise, display a list of available API calls
        return Response(dict({
            "Login": url("login/"),
            "Layout Details": url("details/"),
            "Updates": url("updates/"),
            "Terms": url("terms/"),
            "Grades": url("grades/"),
            "Courses": url("courses/"),
            "Emails": url("emails/"),
            "Calendar": url("calendar/"),
            "Final Exams": url("finals/"),
            "Holds": url("holds/"),
            "Refresh": url("refresh/"),
        }, **(  # If requested path isn't a supported API call, add an error message to indicate it
            {"Error": [request.path + " isn't a supported API call"]} if invalid else {})
        ))
