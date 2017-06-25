from rest_framework.views import APIView
from rest_framework.response import Response
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
        student_id = CharField()
        password = CharField()
    # Register fields description in login API
    serializer_class = Credentials

    # Receives credentials data and preforms login on POST request
    def post(self, request):
        # Store submitted credentials
        sid = request.data.get('student_id')
        pin = request.data.get('password')
        # Try logging in and storing Blackboard cookies
        try: bb_cookies = bb.login(sid, pin)
        # If login fails, store error message instead
        except ConnectionError as error:
            bb_cookies = error.args[0]
        # Display submitted credentials and cookies to viewer (for now)
        return Response({
            'Credentials': sid + ', ' + pin,
            # Send back Blackboard cookies or error message
            'Blackboard Cookie': bb_cookies
        })
