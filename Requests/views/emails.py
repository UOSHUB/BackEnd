from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import outlook


# Student's emails requests handler
class Emails(APIView):
    """
    Emails API root URL
    """
    # Returns list of email related API calls on GET request
    @login_required
    def get(self, request):
        # Provide emails API URL
        url = request.build_absolute_uri
        # Display a list of available email related API calls
        return Response({})
