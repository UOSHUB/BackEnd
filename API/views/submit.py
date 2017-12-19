from rest_framework.response import Response
from rest_framework.views import APIView
from .common import login_required
from Requests import blackboard


# Submission requests handler
class Submit(APIView):
    # Submits sent files to Blackboard on POST request
    @staticmethod
    @login_required("blackboard")
    def post(request, course_id, content_id):
        # Declare a list for formatted files
        files = []
        # Loop maximum of 10 times (10 files)
        for index in range(10):
            # Try to get the file(n) from the sent data
            file = request.data.get("file" + str(index))
            # Stop if there're no more files
            if not file: break
            # Format file in a tuple (name, content, type) then add it to files
            files.append((file.name, file.read(), file.content_type))
        # Return an empty response with whatever status Blackboard returned
        return Response(
            # Submit formatted files to Blackboard
            status=blackboard.edit.submit_files(
                # Send Blackboard cookies
                request.session["blackboard"],
                # And course & content ids and the files
                course_id, content_id, files
            )
        )
