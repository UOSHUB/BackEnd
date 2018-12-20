from rest_framework.response import Response
from Requests.outlook import edit as outlook
from rest_framework.views import APIView
from ..models import Student, KnownGrade
from .common import login_required
from Requests.myudc import reports
from Requests import term_code
from threading import Thread
from time import sleep


# Fetches grades and GPA from transcript
def fetch_grades_and_gpa(student, known_grades=(), loop=0):
    reports._format = "xml"
    try:  # Scrape a list of new grades from reports
        return reports.scrape.grades_and_gpa(
            # Get student's transcript and pass it with the term code
            reports.get.unofficial_transcript(student.sid), term_code, known_grades
        )
    except Exception:
        # If an error occurs, repeat thrice and sleep
        if loop < 3:
            print("sleeping for a while...")
            sleep(4)
            fetch_grades_and_gpa(student, known_grades, loop + 1)

# Subscribe requests handler
class Subscribe(APIView):
    # Gets students dictionary on GET request
    @staticmethod
    def get(request):
        # Returns dictionary of subscribed students with list of their known grades
        return Response({
            student.sid: [grade.course_key for grade in KnownGrade.objects.filter(student=student)]
            for student in Student.objects.all()
        })

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
                # Create and save student in the database
                student = Student(sid=sid)
                student.save()
                # Scrape grades and GPA from transcript report
                reports._format = "xml"
                courses, gpa = fetch_grades_and_gpa(student)
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

    # Checks new grades on PATCH request
    @staticmethod
    def patch(request):
        # Checks grades for all subscribed students
        def check_grades():
            # Loop through all subscribed students
            for sid, known_grades in Subscribe.get(request).data.items():
                # Fetch grades and GPA from transcript
                courses, gpa = fetch_grades_and_gpa(sid, known_grades)
                # Loop though new grades and their courses
                for course_key, course_title, grade, new in courses:
                    # If course grade is new
                    if new:
                        # Send an email announcement to the student about the grade
                        outlook.send_grades_summary(sid, courses, gpa, (grade, course_title))
                        # Add the course of the grade to the database (to be ignored next time)
                        KnownGrade(course_key=course_key, student=Student.objects.get(sid=sid)).save()
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
