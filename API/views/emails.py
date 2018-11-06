from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from .common import login_required, Email
from Requests import outlook


# Student's emails requests handler
class Emails(APIView):
    """
    This returns student's (personal, courses or events) emails,
    which's an dictionary of emails present in the selected category
    """
    # Returns emails array by category on GET request
    @staticmethod
    @login_required()
    def get(request, category, count, offset=0):
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
                        count=count or 20,
                        # Specify numbers of emails to skip (0 by default)
                        offset=offset or 0
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
        @staticmethod
        @login_required()
        def get(request, message_id):
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

        # Deletes an email on DELETE request
        @staticmethod
        @login_required()
        def delete(request, message_id):
            # Return an empty response with status
            # of whether the emails was deleted or not
            return Response(
                # Delete the specified email
                status=outlook.edit.delete_email(
                    # Send student id and password
                    request.session["sid"],
                    request.session["pin"],
                    # Specify message id
                    message_id
                )
            )

    # Email's attachments requests handler
    class Attachment(APIView):
        # Returns email's attachment on GET request
        @staticmethod
        @login_required()
        def get(request, message_id, attachment_id):
            # Return email's decoded attachment
            return HttpResponse(
                # Get email's attachment from Outlook
                **outlook.get.email_attachment(
                    # Send student id and password
                    request.session["sid"],
                    request.session["pin"],
                    # Specify message id & attachment id
                    message_id, attachment_id
                )
            )

    # Email sending requests handler
    class Send(APIView):
        # Sends an email on POST request
        # Register login fields description
        serializer_class = Email

        @staticmethod
        @login_required()
        def post(request):
            # Return the status Outlook's returned
            return Response(
                # Send an email through Outlook
                outlook.edit.send_email(
                    # Send student id and password
                    request.session["sid"],
                    request.session["pin"],
                    # Send email subject, body & recipients
                    request.data["subject"],
                    request.data["body"],
                    request.data["recipients"]
                )
            )
