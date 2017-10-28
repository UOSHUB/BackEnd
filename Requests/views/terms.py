from .common import login_required, client_side
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests import myudc, blackboard
from threading import Thread


# Student's terms requests handler
class Terms(APIView):
    """
    This returns a list of student's registered terms.
    """
    # Returns term dictionary of requested term on GET request
    @staticmethod
    @login_required("myudc")
    def get(request):
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
        # Returns specified term's details
        @staticmethod
        @login_required("myudc")
        def get(request, term):
            # Return student's term details
            return Response(dict({} if client_side(request) else {
                # Add links to term's contents and courses if browser
                "Deadlines": request.build_absolute_uri("deadlines/"),
                "Documents": request.build_absolute_uri("documents/"),
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
        # Returns term's content or courses as per request
        @staticmethod
        @login_required("blackboard")
        def get(request, term, data_type):
            # If data type requested is "courses"
            if data_type == "courses":
                # Return a dictionary of courses ids
                return Response(
                    # Get & scrape courses' ids from Blackboard by term
                    blackboard.scrape.courses_by_term(
                        blackboard.get.courses_list(
                            # Send Blackboard cookies
                            request.session["blackboard"]
                        ), term  # Send term id
                    )
                )
            # If data type requested is "deadlines" or "documents"
            else:
                # Initialize empty arrays & store Blackboard cookies
                content, threads = [], []
                cookies = request.session["blackboard"]

                # A single course's content fetching function for threading
                def course_data(course_key, course_id):
                    # Get & scrape course's data then add it to content
                    content.extend(
                        blackboard.scrape.course_data(
                            blackboard.get.course_data(
                                # Send Blackboard cookies & course id to get
                                cookies, course_id
                                # Send requested type & MyUDC course id to scrape
                            ), course_key, data_type
                        )
                    )
                # Get & scrape then loop through Blackboard courses in term
                for key, course in blackboard.scrape.courses_by_term(
                    # Send Blackboard cookies to "get" and term id to "scrape"
                    blackboard.get.courses_list(cookies), term
                ).items():
                    # Construct a thread to get each course's data in parallel
                    thread = Thread(target=course_data, args=(key, course["courseId"]))
                    # Start the thread and add it to threads
                    thread.start()
                    threads.append(thread)
                # Loop through all threads and join them to main thread
                [thread.join() for thread in threads]
                # Return all courses' content after all threads are done
                return Response(content)
