from rest_framework.response import Response
from Requests.outlook import edit as outlook
from rest_framework.views import APIView
from ..models import Student, KnownGrade
from .common import login_required
from Requests.myudc import reports
from Requests import term_code
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
                outlook.send_grades_summary(sid, courses, gpa)
            # Execute subscription process on a new thread
            Thread(target=subscribe, daemon=True).start()
            # Return CREATED response
            return Response(status=201)
        # Otherwise return ALREADY REPORTED response
        return Response(status=208)

    @staticmethod
    def patch(request):
        # Checks grades for all subscribed students
        def check_grades():
            # Loop through all subscribed students
            for student in Student.objects.all():
                # Scrape a list of new grades from reports
                reports._format = "xml"
                courses, gpa = reports.scrape.grades_and_gpa(
                    # Get student's transcript and pass it with the term code
                    reports.get.unofficial_transcript(student.sid), term_code,
                    # Also, pass it a list of student's already known grades from database
                    [grade.course_key for grade in KnownGrade.objects.filter(student=student)]
                )
                # Loop though new grades and their courses
                for course_key, course_title, grade, new in courses:
                    # If course grade is new
                    if new:
                        # Send an email announcement to the student about the grade
                        outlook.send_grades_summary(student.sid, courses, gpa, (grade, course_title))
                        # Add the course of the grade to the database (to be ignored next time)
                        KnownGrade(course_key=course_key, student=student).save()
        # Execute grades checking process on a new thread
        Thread(target=check_grades, daemon=True).start()
        # Return OK
        return Response()

    # Unsubscribe from services on DELETE request
    @staticmethod
    @login_required()
    def delete(request):
        # Store current student database model object
        student = Student.objects.filter(sid=request.session["sid"])
        # If student is stored among the subscribers
        if student.exists():
            # Remove student from the database
            student.delete()
            # Return NO CONTENT response
            return Response(status=204)
        # Otherwise return GONE response
        return Response(status=410)
