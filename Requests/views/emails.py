from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import outlook


# Student's emails requests handler
class Emails(APIView):
    """
    Emails API root URL
    """
    # Returns list of email related API calls on GET request
    @login_required
    def get(self, request):
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
