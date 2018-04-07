from .common import login_required
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests.myudc import reports
from Requests import myudc


# Student's schedule designing requests handler
class Design(APIView):
    """
    This returns a list of student's registrable courses.
    """
    # Returns all registrable courses on GET request
    @staticmethod
    @login_required("myudc")
    def get(request, term_code):
        # Get & scrape all remaining courses
        remaining = reports.scrape.remaining_courses(
            reports.get.study_plan(
                request.session["sid"],
                "201410"
            )
        )
        subjects = set(course[:4] for course in remaining["courses"])
        # Return all registrable courses
        return Response(
            myudc.scrape.registrable_courses_from_all(
                myudc.get.all_offered_courses(
                    request.session["myudc"],
                    # subjects
                ), subjects
            )
        )
