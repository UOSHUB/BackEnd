from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Student, KnownGrade
from Requests import zoho, term_code
from .common import login_required
from Requests.myudc import reports
from threading import Thread


# Subscribe requests handler
class Subscribe(APIView):
    # Subscribe to services on POST request
    @staticmethod
    @login_required()
    def post(request):
        # Store current student id
        sid = request.session["sid"]
        # If student isn't stored among the subscribers
        if not Student.objects.filter(sid=sid).exists():
            # Subscribes student and sends grades summary email
            def subscribe():
                reports._format = "xml"
                # Scrape grades and GPA from transcript report
                courses, gpa = reports.scrape.grades_and_gpa(
                    # Get student's transcript and pass it with the term code
                    reports.get.unofficial_transcript(sid), term_code
                )
                # Create and save student in the database
                student = Student(sid=sid)
                student.save()
                # Loop through all courses
                for course in courses:
                    # Store all of them as known grades in the database
                    KnownGrade(student=student, course_key=course[0]).save()
                # Send an email with grades and GPA summary
                zoho.send.grades_summary(sid, courses, gpa)
            # Execute subscription process on a new thread
            Thread(target=subscribe, daemon=True).start()
            # Return CREATED response
            return Response(status=201)
        # Otherwise return ALREADY REPORTED response
        return Response(status=208)

    # Unsubscribe from services on DELETE request
    @staticmethod
    @login_required()
    def delete(request):
        # Store current student database model object
        student = Student.objects.filter(sid=request.session["sid"])[0]
        # If student is stored among the subscribers
        if student.exists():
            # Remove student from the database
            student.delete()
            # Return NO CONTENT response
            return Response(status=204)
        # Otherwise return GONE response
        return Response(status=410)
