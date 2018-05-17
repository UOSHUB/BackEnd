from Requests.myudc import reports
from Requests.zoho import send
from Requests import term_code
from datetime import datetime
from threading import Thread
from time import sleep
import os


# Checks for new grades every 20 minutes during the day
def check_grades(once=False):
    # Import database models here to avoid early run errors
    from .models import Student, KnownGrade
    # Loop infinitely
    while True:
        # Store current date & time
        now = datetime.now()
        # Refresh timestamp in environment
        os.environ["timestamp"] = str(now.timestamp())
        # Loop through all subscribed students
        for student in Student.objects.all():
            # Scrape a list of new grades from reports
            new_grades = reports.scrape.new_grades(
                # Get student's transcript and pass it with the term code
                reports.get.unofficial_transcript(student.sid), term_code,
                # Also, pass it a list of student's already known grades from database
                [grade.course_key for grade in KnownGrade.objects.all()]
            )
            # If there are any new grades
            if len(new_grades) > 0:
                # Loop though new grades and their courses
                for course_key, course_title, grade in new_grades:
                    # Send an email announcement to the student about the grade
                    send.grade_announcement(student.sid, course_title, grade)
                    # Add the course of the grade to the database (to be ignored next time)
                    KnownGrade(course_key=course_key, student=student).save()
        # Break if only once
        if once: break
        # If it's after midnight
        elif 0 < now.hour < 7:
            # Sleep until the morning
            sleep((now.replace(hour=7, minute=0, second=0) - now).total_seconds())
        # Otherwise, sleep for 20 minutes
        else: sleep(1200)


# Starts a thread to check grades when first run
def start_grades_checking():
    # If timestamp doesn't exist or it hasn't been 10 seconds since last run (to avoid Django double run)
    if datetime.now().timestamp() - float(os.environ.get("timestamp", 0)) > 10:
        # Start a thread to check for new grades
        Thread(target=check_grades).start()
