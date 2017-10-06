from .common import login_required, client_side
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests import myudc, blackboard


# Student's terms requests handler
class Terms(APIView):
    """
    This returns a list of student's registered terms.
    """
    server = "myudc"

    # Returns term dictionary of requested term on GET request
    @login_required
    def get(self, request):
        # Get & scrape all registered terms
        terms = myudc.scrape.registered_terms(
            myudc.get.reg_history(
                # Send myUDC cookies
                request.session["myudc"]
            )
        )
        # Return all terms
        return Response({
            # In {term code: {}} pairs
            term: {} for term in terms.keys()
            # If requested from the client side
        } if client_side(request) else {
            # Then make it in {term name: term url} pairs
            name: request.build_absolute_uri(code + "/")
            # By looping through all terms and formatting them
            for code, name in terms.items()
        })

    # Term's Blackboard content handler
    class Details(APIView):
        """
        This returns student's term details,
        which's a dictionary of courses' data.
        """
        server = "myudc"

        # Returns specified term's details
        @login_required
        def get(self, request, term):
            # Return student's term details
            return Response(dict({} if client_side(request) else {
                # Add links to term's content and courses if browser
                "Content": request.build_absolute_uri("content/"),
                "Courses": request.build_absolute_uri("courses/")
            },  # Get & scrape student's term from myUDC
                **myudc.scrape.term(
                    myudc.get.term(
                        # Send term code & myUDC cookies
                        term, request.session["myudc"]
                    )
                )
            ))

    # Term's Blackboard content handler
    class Content(APIView):
        """
        This returns student's term content or courses,
        which's a dictionary of courses' documents & deadlines
        or a list of term's courses with all their ids.
        """
        server = "blackboard"

        # Returns term's content or courses as per request
        @login_required
        def get(self, request, term, data_type):
            # If data type requested is "content"
            if data_type == "content":
                # Return a dictionary of all courses' content
                return Response({
                    # Get & scrape course's data from Blackboard Mobile
                    key: dict(course, **blackboard.scrape.course_data(
                        blackboard.get.course_data(
                            # Send Blackboard cookies & course blackboard id
                            request.session["blackboard"], course["bb"]
                        )
                    ))
                    # Get & scrape then loop through courses in requested term
                    for key, course in blackboard.scrape.courses_by_term(
                        blackboard.get.courses_list(
                            # Send Blackboard cookies
                            request.session["blackboard"]
                        ), term  # Send term id
                    ).items()
                })
            # If data type requested is "courses"
            elif data_type == "courses":
                # Return a dictionary of courses ids
                return Response(
                    blackboard.scrape.courses_by_term(
                        blackboard.get.courses_list(
                            # Send Blackboard cookies
                            request.session["blackboard"]
                        ), term  # Send term id
                    )
                )
