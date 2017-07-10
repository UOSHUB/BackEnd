from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.serializers import Serializer, CharField, BooleanField
from . import myudc as udc, blackboard as bb, reports as rep


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
            "Login": url("login/")
        })


# Login and session requests handler
class Login(APIView):
    """
    Login to UOSHUB
    {Sid: Student Id, Pin: Password, New: whether it's the first login or not}
    """
    # Describes login credentials fields
    class Credentials(Serializer):
        sid = CharField()
        pin = CharField()
        new = BooleanField()
    # Register fields description in login API
    serializer_class = Credentials

    # Receives credentials data and preforms login on POST request
    def post(self, request):
        # Store submitted credentials
        sid = request.data.get('sid')
        pin = request.data.get('pin')
        # Try logging in and storing Blackboard cookies
        try: bb_cookies = bb.login(sid, pin)
        # If login to Blackboard fails
        except ConnectionError as error:
            # Return error message with BAD_REQUEST status
            return Response(error.args[0], status=400)
        # Prepare cookies by storing submitted credentials and blackboard cookies
        cookies = {'uoshub': {'sid': sid, 'pin': pin}, 'blackboard': bb_cookies}
        # Prepare response and set cookies
        response = Response({})
        response.set_cookie("login", cookies)
        # If API is being requested from a browser
        if isinstance(request.accepted_renderer, BrowsableAPIRenderer):
            # Display cookies in viewer browser (for now)
            response.data['cookies'] = cookies
        # If this is student's first login
        if request.data.get('new'):
            # Return student's core details (dummy for now)
            response.data.update(rep.scrape.core_details(rep.get.unofficial_transcript(sid)))
        return response
