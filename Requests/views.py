from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import Serializer, CharField
from . import myudc as udc, blackboard as bb, reports as rep


# API root (/api/) requests handler
class APIRoot(APIView):
    """ UOSHUB Restful API Root URL"""
    # Returns list of available API calls on GET request
    def get(self, request):
        url = request.build_absolute_uri
        return Response([
            {"Login": url("login/")},
            "Notice that all API calls require login first except for calendar calls"
        ])


# Login and session requests handler
class Login(APIView):
    """ LOGIN TO UOSHUB """
    # Describes login credentials fields
    class Credentials(Serializer):
        username = CharField(max_length=9)
        password = CharField(max_length=6)
    # Register fields description in login API
    serializer_class = Credentials

    # Receives credentials data and preforms login on POST request
    def post(self, request):
        # Store getter function of submitted data
        get = request.data.get
        # Display submitted credentials to viewer (for now)
        return Response({
            'Username': get('username'),
            'Password': get('password')
        })
