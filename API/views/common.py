from rest_framework.renderers import BrowsableAPIRenderer as __Browser
from rest_framework.serializers import Serializer, CharField, EmailField
from rest_framework.response import Response
from Requests import blackboard, myudc
from django.shortcuts import redirect
from time import time


# Describes login credentials fields
class Credentials(Serializer):
    sid = CharField()
    pin = CharField()


# Describes an email fields
class Email(Serializer):
    subject = CharField()
    body = CharField()
    recipients = EmailField()


# Returns a login checker decorator by server
def login_required(server=None):
    # A decorator for methods that require login
    def decorator(method):
        # Checks login status and responds accordingly
        def checker(request, *args, **kwargs):
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
            elif server and time() - session.get(server + "_time", 0) > 14*60:
                # TODO: keep blackboard and myudc cookies on the client side and get them from it
                # Update session's login cookies and timestamp
                session.update({
                    # Login to server again depending on the method
                    server: globals()[server].login(
                        # Send current student id and password
                        session["sid"], session["pin"]
                        # Store new login timestamp
                    ), server + "_time": time()
                })
            # Once logged in, proceed to method execution
            return method(request, *args, **kwargs)
        return checker
    return decorator


# Returns whether the request is from client-side or not
def client_side(request):
    # If request renderer isn't browser, consider it from client-side
    return not isinstance(request.accepted_renderer, __Browser)
