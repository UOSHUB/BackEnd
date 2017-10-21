from requests.exceptions import ConnectionError as NoConnectionError
from .common import Credentials, login_required, client_side
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests import blackboard, outlook
from django.shortcuts import redirect
from time import time


# Login requests handler
class Login(APIView):
    """
    Login to UOSHUB
    {Sid: Student Id, Pin: Password}
    """
    # Register login fields description
    serializer_class = Credentials

    # Receives credentials data and preforms login on POST request
    def post(self, request):
        # Store submitted credentials
        sid = request.data.get("sid")
        pin = request.data.get("pin")
        # Login to outlook, if credentials are wrong
        if not outlook.login(sid, pin):
            # Return error message with BAD_REQUEST status
            return Response("Wrong Credentials!", status=400)
        # Store submitted credentials in session
        request.session.update({"sid": sid, "pin": pin})
        # Return an empty response indicating success, or go to GET if browser
        return Response() if client_side(request) else redirect(request.path)

    # Returns login session/status on GET request
    def get(self, request):
        # Return "You're not logged in!" if so, otherwise return session
        return Response({
            "sessionId": request.session.session_key or "You're not logged in!"
        })

    # Logout by deleting login session
    @login_required()
    def delete(self, request):
        # Clear student session
        request.session.flush()
        # Return an empty response indicating success, or go to GET if browser
        return Response() if client_side(request) else self.get(request)
