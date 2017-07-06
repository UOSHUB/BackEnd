from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.serializers import Serializer, CharField
from . import myudc as udc, blackboard as bb, reports as rep


# API root (/api/) requests handler
class APIRoot(APIView):
    """ UOSHUB Restful API Root URL """
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
        sid = CharField()
        pin = CharField()
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
        response = Response()
        response.set_cookie("login", cookies)
        # If API is being requested from a browser
        if isinstance(request.accepted_renderer, BrowsableAPIRenderer):
            # Display cookies in viewer browser (for now)
            response.data = cookies
        return response
