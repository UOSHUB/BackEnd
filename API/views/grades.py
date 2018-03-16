from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import blackboard
from threading import Thread


# Grades requests handler
class Grades(APIView):
    """
    This returns student's Blackboard grades,
    which's an array of grades' details.
    """
    # Returns student's array of grades on GET request
    @staticmethod
    @login_required("blackboard")
    def get(request, term_code):
        # If requesting grades of a term
        if term_code:
            # Initialize empty objects & store Blackboard cookies
            grades, threads = [], []
            cookies = request.session["blackboard"]
            sid = request.session["sid"]

            # A single course's grades fetching function for threading
            def course_grades(course_key, course_id):
                # Get & scrape then add course's grades to dictionary
                grades.extend(
                    blackboard.scrape.course_grades(
                        blackboard.get.course_grades(
                            # Send Blackboard cookies, sid & course id
                            cookies, sid, course_id
                        ), course_key
                    )
                )
            # Get & scrape then loop through Blackboard courses in term
            for key, course in blackboard.scrape.courses_by_term(
                # Send Blackboard cookies to "get" and term id to "scrape"
                blackboard.get.courses_list(cookies), term_code
            ).items():
                # Construct a thread to get each course's grades in parallel
                thread = Thread(target=course_grades, args=(key, course["courseId"]))
                # Start the thread and add it to threads
                thread.start()
                threads.append(thread)
            # Loop through all threads and join them to main thread
            [thread.join() for thread in threads]
            # Return all courses' grades after all threads are done
            return Response(grades)
        # If requesting grades API root path
        return Response({
            # Return a dictionary of {term name: url of grades in term} pairs
            term_name: request.build_absolute_uri(term_code + "/")
            # Get & scrape then loop through available terms in Blackboard
            for term_name, term_code in blackboard.scrape.terms_list(
                blackboard.get.courses_list(
                    request.session["blackboard"]
                )
            ).items()
        })
