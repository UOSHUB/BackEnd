from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import blackboard


# Student's courses requests handler
class Courses(APIView):
    server = "blackboard"
    """
    Courses API root URL
    A list of all courses registered in Blackboard
    """
    # Returns a list of courses or course's data (with term and data type options)
    @login_required
    def get(self, request, course=None, term=None, data_type=None):
        # If a specific course is requested
        if course:
            # Return requested course's data
            return Response(
                # Get & scrape course's data from Blackboard Mobile
                blackboard.scrape.course_data(
                    blackboard.get.course_data(
                        # Send Blackboard cookies
                        request.session["blackboard"],
                        # Send course id
                        course
                    ),  # Send requested data type
                    data_type  # "documents" or "deadlines"
                )
            )
        # If all courses in term are requested
        if term:
            # Return a dictionary of all courses' data
            return Response({
                # Get & scrape course's data from Blackboard Mobile
                course: blackboard.scrape.course_data(
                        blackboard.get.course_data(
                            # Send Blackboard cookies
                            request.session["blackboard"],
                            # Send course id
                            course
                        ),  # Send requested data type
                        data_type  # "documents" or "deadlines"
                    )
                # Get & scrape then loop through courses in requested term
                for course in blackboard.scrape.courses_by_term(
                    blackboard.get.courses_list(
                        # Send Blackboard cookies
                        request.session["blackboard"]
                    ),  # Send term id
                    term
                )
            })
        # If course and term aren't specified, return student's courses
        return Response(
            # Get & scrape courses list from Blackboard Mobile
            blackboard.scrape.courses_list(
                blackboard.get.courses_list(
                    # Send Blackboard cookies
                    request.session["blackboard"]
                ),  # Send scrape the URL builder
                lambda path: request.build_absolute_uri(path + "/")
            )
        )