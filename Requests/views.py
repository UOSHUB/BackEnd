from rest_framework.views import APIView
from rest_framework.response import Response
from . import myudc as udc, blackboard as bb, reports as rep


# API root (/api/) requests handler
class APIRoot(APIView):
    """ UOSHUB Restful API Root URL"""
    # Returns list of available API calls on GET request
    def get(self, request):
        return Response([
            "Notice that all API calls require login first except for calendar calls"
        ])
