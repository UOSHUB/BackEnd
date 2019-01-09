from .common import Credentials, login_required, client_side
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from Requests import blackboard
from time import time
# from ..models import Student


# Login requests handler
class Login(APIView):
    """
    Login to UOSHUB
    {Sid: Student Id, Pin: Password}
    """
    # Register login fields description
    serializer_class = Credentials

    # Receives credentials data and preforms login on POST request
    @staticmethod
    def post(request):
        # Store submitted credentials
        sid = request.data.get("sid").upper()
        pin = request.data.get("pin")
        # Try logging in to Blackboard
        try: cookies = blackboard.login(sid, pin)
        except Exception as error:
            # If it failed, return error message with BAD_REQUEST status
            return Response(str(error), status=400)
        # Store submitted credentials and Blackboard cookies in session
        request.session.update({"sid": sid, "pin": pin, "blackboard": cookies, "blackboard_time": time()})
        # Return empty response indicating success, or go to GET if from API
        return Response({
            # "subscribed": Student.objects.filter(sid__iexact=sid).exists()
        }) if client_side(request) else redirect(request.path)

    # Returns login session/status on GET request
    @staticmethod
    def get(request):
        # Return "You're not logged in!" if so, otherwise return session
        return Response({
            "sessionId": request.session.session_key or "You're not logged in!"
        })

    # Logout by deleting login session
    @staticmethod
    @login_required()
    def delete(request):
        # Clear student session
        request.session.flush()
        # Return an empty response indicating success, or go to GET if browser
        return Response() if client_side(request) else Login.get(request)
