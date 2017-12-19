from rest_framework.response import Response
from rest_framework.views import APIView
from API.models import Student
from .common import login_required


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
            # Save student in the database
            Student(sid=sid).save()
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
