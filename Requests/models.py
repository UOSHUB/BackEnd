from django.db import models
from django.contrib.admin import site


# A database class describing a student
class Student(models.Model):
    # Student id as a 9 characters primary key
    sid = models.CharField(max_length=9, primary_key=True)

    # Display student id on print
    def __str__(self):
        return self.sid


# A database class describing a student's known course grade
class KnownGrade(models.Model):
    # Course MyUDC key as a 7 digits primary key
    course_key = models.CharField(max_length=7, primary_key=True)
    # Link known grade to its student with its id as a foreign key
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # Display course key and student id on print
    def __str__(self):
        return self.course_key + " for " + self.student.sid


# Register database classes in the admin panel
site.register([Student, KnownGrade])
