from rest_framework.response import Response
from Requests.outlook import edit as outlook
from rest_framework.views import APIView
from ..models import Student, KnownGrade
from .common import login_required
from Requests.myudc import reports
from Requests import term_code
from time import sleep, ctime
from threading import Thread
from requests import get


# Subscribe requests handler
class Subscribe(APIView):
    # Gets students dictionary on GET request
    @staticmethod
    def get(request):
        # Returns a list of all subscribed students
        return Response([student.sid for student in Student.objects.all()])

    # Subscribe to services on POST request
    @staticmethod
    @login_required()
    def post(request):
        # Store current student id
        sid = request.session["sid"]
        # If student isn't stored among the subscribers
        if not Student.objects.filter(sid__iexact=sid).exists():
            # Save student to the database
            Student(sid=sid).save()
            print("Subscribed", sid)
            # Return CREATED response
            return Response(status=201)
        # Otherwise return ALREADY REPORTED response
        return Response(status=208)

    # Checks new grades on PATCH request
    @staticmethod
    def patch(request):
        # Fetches student's grades and GPA from transcript
        def fetch_grades_and_gpa(sid, loop=0):
            reports._format = "xml"
            try:  # Scrape a list of grades from reports
                return reports.scrape.grades_and_gpa(
                    # Get student's transcript and pass it with the term code
                    reports.get.unofficial_transcript(sid), term_code
                )
            except Exception as error:
                # If an error occurs, repeat thrice and sleep
                if loop < 3:
                    print("Error:", error, "sleeping for a while...")
                    sleep(4)
                    fetch_grades_and_gpa(sid, loop + 1)

        # Checks grades for all subscribed students
        def check_grades():
            print("\nStarted grades checker on", ctime())
            try: students = get("https://uoshub.com/api/subscribe/").json()
            except:
                students = Subscribe.get(request).data
                print("\nUOSHUB IS DOWN!\n")
            # Loop through all subscribed students
            for index, sid in enumerate(students):
                print(f"Checking grades for {sid} #{index + 1}", end="\r")
                # Fetch grades and GPA from transcript
                courses, gpa = fetch_grades_and_gpa(sid)
                # If student is new
                if not Student.objects.filter(sid__iexact=sid).exists():
                    # Save him to local database
                    student = Student(sid=sid)
                    student.save()
                    # Send him a subscribed message
                    outlook.send_grades_summary(sid, courses, gpa)
                    # Save already out grades as known
                    [KnownGrade(course_key=course[0], student=student).save() for course in courses]
                    continue
                # Otherwise, get his known grades from local db
                student = Student.objects.get(sid__iexact=sid)
                known_grades = [grade.course_key for grade in KnownGrade.objects.filter(student=student)]
                # Loop though new grades and their courses
                for course_key, course_title, grade in courses:
                    # If course grade is new
                    if course_key not in known_grades:
                        # Send an email announcement to the student about the new grade
                        outlook.send_grades_summary(sid, courses, gpa, (grade, course_title))
                        # Add the course of the grade to the database (to be ignored next time)
                        KnownGrade(course_key=course_key, student=student).save()
            print("Ended grades checker on", ctime())
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
