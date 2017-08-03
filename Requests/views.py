from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.serializers import Serializer, CharField
from . import myudc as udc, blackboard as bb, reports as rep, outlook as ms


# API root (/api/) requests handler
class APIRoot(APIView):
    """
    UOSHUB Restful API root URL.
    Notice that all API calls require login first except for calendar calls.
    """
    # Returns list of available API calls on GET request
    def get(self, request):
        # Provide full API URL to current server
        url = request.build_absolute_uri
        # Display a list of available API calls
        return Response({
            "Login": url("login/"),
            "Core Details": url("details/"),
        })


# Login requests handler
class Login(APIView):
    """
    Login to UOSHUB
    {Sid: Student Id, Pin: Password, New: whether it's the first login or not}
    """
    # Describes login credentials fields
    class Credentials(Serializer):
        sid = CharField()
        pin = CharField()
    # Register fields description in login API
    serializer_class = Credentials

    # Receives credentials data and preforms login on POST request
    def post(self, request):
        # Store submitted credentials
        sid = request.data.get('sid')
        pin = request.data.get('pin')
        # Login to outlook, if credentials are wrong
        if not ms.login(sid, pin):
            # Return error message with BAD_REQUEST status
            return Response("Wrong Credentials!", status=400)
        # Establish a session by storing submitted credentials
        request.session['uoshub'] = {'sid': sid, 'pin': pin}
        # If API is being requested from a browser
        if isinstance(request.accepted_renderer, BrowsableAPIRenderer):
            # Display Django session id in viewer's browser
            return Response({'session_id': request.session.session_key})
        # Otherwise, return an empty response indicating success
        return Response()


# Core student details requests handler
class CoreDetails(APIView):
    # Returns student's core details on GET request
    def get(self, request):
        # Return student's core details
        return Response(
            # Scrape core details
            rep.scrape.core_details(
                # Get student's transcript
                rep.get.unofficial_transcript(
                    # Pass student id from session
                    request.session['uoshub']['sid']
                )
            )
        )
