from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests import blackboard, myudc
from .common import login_required
from .api_root import APIRoot


# Student's courses requests handler
class Courses(APIView):
    """
    This returns course's data, which is a list
    of documents and deadline in the course
    """
    # Returns a list of courses or course's data (with term and data type options)
    @staticmethod
    @login_required("blackboard")
    def get(request):
        # Return list of student's courses
        return Response(
            # Get & scrape courses list from Blackboard Mobile
            blackboard.scrape.courses_list(
                blackboard.get.courses_list(
                    # Send Blackboard cookies
                    request.session["blackboard"]
                ),  # Send scrape the URL builder
                lambda path: request.build_absolute_uri("/api/courses/" + path + "/")
            )
        )

    # Course's Blackboard content handler
    class Content(APIView):
        """
        This returns course's Blackboard content,
        which includes its documents and deadlines
        """
        # Returns course's documents and deadlines
        @staticmethod
        @login_required("blackboard")
        def get(request, course_key, course_id):
            # Return requested course's data
            return Response(
                # Get & scrape course's data from Blackboard Mobile
                blackboard.scrape.course_data(
                    blackboard.get.course_data(
                        # Send Blackboard cookies & course's id
                        request.session["blackboard"], course_id
                    ), course_key, course_id
                )
            )

    # Course's MyUDC details handler
    class Details(APIView):
        """
        Returns course's MyUDC details,
        which includes its location, time, doctor, etc...
        """
        # Returns a single course's details
        @staticmethod
        @login_required("myudc")
        def get(request, course_key, crn, term_code):
            # If crn or term aren't sent
            if not (crn and term_code):
                # Return to API root with an error message
                return APIRoot.get(request, request.path)
            # Otherwise, return requested course's details
            return Response(
                # Get & scrape course's details from MyUDC
                myudc.scrape.course(
                    myudc.get.course(
                        # Send MyUDC session
                        request.session["myudc"],
                        # Send course's key, crn and term code
                        crn, course_key, term_code
                    )
                )
            )

    # Course's Blackboard document download handler
    class Documents(APIView):
        """
        Downloads a course's document file
        """
        # Returns a course's document file
        @staticmethod
        @login_required("blackboard")
        def get(request, content_id, xid):
            # Get course document data and name from Blackboard
            file_data, file_name = blackboard.get.course_document(
                # Send Blackboard cookies
                request.session["blackboard"],
                # Send document content id and xid
                content_id, xid
            )
            # Construct a response with document content and type
            response = HttpResponse(**file_data)
            # Specify document file name in response and return it
            response["Content-Disposition"] = f'attachment; filename="{file_name}"'
            return response
