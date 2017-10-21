from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import outlook


# Student's emails requests handler
class Emails(APIView):
    """
    This returns student's (personal, courses or events) emails,
    which's an dictionary of emails present in the selected category
    """
    # Returns emails array by category on GET request
    @login_required()
    def get(self, request, category, count):
        # If emails category is requested
        if category:
            # Return array of requested emails
            return Response(
                # Get & scrape emails from requested category
                getattr(outlook.scrape, category + "_emails")(
                    outlook.get.emails_list(
                        # Send student id and password
                        request.session["sid"],
                        request.session["pin"],
                        # Specify emails category
                        search=category,
                        # Specify emails count (20 by default)
                        count=count or 20
                    )
                )
            )
        # If emails API root is requested
        # Provide emails API URL
        url = request.build_absolute_uri
        # Display a list of available email related API calls
        return Response({
            "Personal": url("personal/"),
            "Courses": url("courses/"),
            "Events": url("events/")
        })

    # Email's body requests handler
    class Body(APIView):
        """
        This returns email's HTML content,
        after embedding its images in it (if any)
        """
        # Returns email's HTML content on GET request
        @login_required()
        def get(self, request, message_id):
            # Return email's body string
            return Response(
                # Get & scrape email's body
                outlook.scrape.email_body(
                    outlook.get.email_body(
                        # Send student id and password
                        request.session["sid"],
                        request.session["pin"],
                        # Specify message id
                        message_id
                    )
                )
            )
