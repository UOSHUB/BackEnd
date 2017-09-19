from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.serializers import Serializer, CharField
from requests.exceptions import ConnectionError as NoConnectionError
from . import myudc, blackboard, outlook
from time import time


# A decorator for methods that require login
def login_required(method):
    # Checks login status and responds accordingly
    def checker(api, request, *args, **kwargs):
        session = request.session
        # If student has never logged in
        if not session.get("sid"):
            # If requesting from browser
            if not client_side(request):
                # Redirect to login page
                return redirect("/api/login/")
            else:  # Otherwise, Return error message with UNAUTHORIZED status
                return Response("You're not logged in!", status=401)
        # If method is dependent on server's session and it's been more that 14 minutes
        elif hasattr(api, "server") and time() - session.get(api.server + "_time", 0) > 14*60:
            # Update session's login cookies and timestamp
            session.update({
                # Login to server again depending on the method
                api.server: globals()[api.server].login(
                    # Send current student id and password
                    session["sid"], session["pin"]
                    # Store new login timestamp
                ), api.server + "_time": time()
            })
        # Once logged in, proceed to method execution
        return method(api, request, *args, **kwargs)
    return checker


# Returns whether the request is from client-side or not
def client_side(request):
    # If request renderer isn't browser, consider it from client-side
    return not isinstance(request.accepted_renderer, BrowsableAPIRenderer)


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
            "Layout Details": url("details/"),
            "Updates": url("updates/"),
            "Schedule": url("schedule/"),
            "Emails": url("emails/"),
        })


# Login requests handler
class Login(APIView):
    """
    Login to UOSHUB
    {Sid: Student Id, Pin: Password}
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
        sid = request.data.get("sid")
        pin = request.data.get("pin")
        # Try logging in to Blackboard
        try: request.session.update({
                # Store its cookies in session
                "blackboard": blackboard.login(sid, pin),
                # Store login timestamp
                "blackboard_time": time()
            })
        # If login to Blackboard fails
        except ConnectionError as error:
            # Return error message with BAD_REQUEST status
            return Response(error.args[0], status=400)
        # If Blackboard is down
        except NoConnectionError:
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
        # Return "You're not logged in!" if so, otherwise return session id
        return Response({
            "sessionId": request.session.session_key or "You're not logged in!"
        })


# Website's layout details requests handler
class LayoutDetails(APIView):
    server = "blackboard"
    """
    This only returns student's basic info right now,
    but in the future it will have all layout details including:
    theme preferences, student's modifications and other settings
    """
    # Returns layout details on GET request
    @login_required
    def get(self, request):
        # Return student's basic info as of now
        return Response({
            # Get student's basic info from Blackboard
            "student": blackboard.api.basic_info(
                # Send Blackboard cookies
                request.session["blackboard"],
                # And current student id
                request.session["sid"]
            )
        })


# Student's updates requests handler
class Updates(APIView):
    server = "blackboard"
    """
    This returns student's Blackboard updates,
    which is a dictionary of updates and the
    names of the courses they are coming from.
    """
    # Returns updates dictionary of all courses on GET request
    @login_required
    def get(self, request):
        # Return updates object
        return Response(
            # Get & scrape student's updates from Blackboard
            blackboard.scrape.updates(
                blackboard.get.updates(
                    # Send Blackboard cookies
                    request.session["blackboard"]
                )
            )
        )


# Student's schedule requests handler
class Schedule(APIView):
    server = "myudc"
    """
    This returns student's schedule details,
    which's a dictionary of courses that contain:
    course id, title, days, time, crn, location, etc..
    """
    # Returns schedule dictionary of requested term on GET request
    @login_required
    def get(self, request, term=None):
        # If accessing "/schedule" without specifying term
        if not term:
            # Get & scrape all registered terms
            terms = myudc.scrape.registered_terms(
                myudc.get.reg_history(
                    # Send myUDC cookies
                    request.session["myudc"]
                )
            )
            # Return all terms as {term code: term name} pairs
            return Response(terms if client_side(request) else {
                # Unless it's a browser, then make it {term name: term url} pairs
                name: request.build_absolute_uri(code)
                # By looping through all terms and formatting them
                for code, name in terms.items()
            })
        # Return student's schedule details
        return Response(
            # Get & scrape student's schedule from myUDC
            myudc.scrape.schedule(
                myudc.get.schedule(
                    # Send term code & myUDC cookies
                    term, request.session["myudc"]
                )
            )
        )


# Student's emails requests handler
class Emails(APIView):
    """
    Emails API root URL
    """
    # Returns list of email related API calls on GET request
    @login_required
    def get(self, request):
        # If URL isn't ending with trailing slash
        if not request.path.endswith("/"):
            # Redirect to one with trailing slash
            return redirect("emails/")
        # Provide emails API URL
        url = request.build_absolute_uri
        # Display a list of available email related API calls
        return Response({
            "Previews": url("previews/"),
        })

    # Student's emails previews handler
    class Previews(APIView):
        """
        This returns previews of student's emails,
        which's a dictionary of email reviews that only contain:
        title, event, time and sender.
        """
        # Returns a dictionary of emails previews on GET request
        @login_required
        def get(self, request):
            # Return student's emails previews
            return Response(
                # Get & scrape student's emails previews from Outlook
                outlook.scrape.emails_previews(
                    outlook.get_emails(
                        # Send current student id
                        request.session["sid"],
                        # And his password
                        request.session["pin"],
                        # Only get the 10 latest emails
                        count=10
                    )
                )
            )
