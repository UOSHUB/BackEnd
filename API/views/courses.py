from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests import blackboard, myudc
from .common import login_required
from .api_root import APIRoot
from threading import Thread
from zipfile import ZipFile


# Student's courses requests handler
class Courses(APIView):
    """
    This returns course's data, which is a list
    of documents and deadline in the course
    """
    # Returns a list of courses or course's data (with term and data type options)
    @staticmethod
    @login_required("blackboard")
    def get(request):
        # Return list of student's courses
        return Response(
            # Get & scrape courses list from Blackboard Mobile
            blackboard.scrape.courses_list(
                blackboard.get.courses_list(
                    # Send Blackboard cookies
                    request.session["blackboard"]
                ),  # Send scrape the URL builder
                lambda path: request.build_absolute_uri("/api/courses/" + path + "/")
            )
        )

    # Course's Blackboard content handler
    class Content(APIView):
        """
        This returns course's Blackboard content,
        which includes its documents and deadlines
        """
        # Returns course's documents and deadlines
        @staticmethod
        @login_required("blackboard")
        def get(request, course_key, course_id):
            # Return requested course's data
            return Response(
                # Get & scrape course's data from Blackboard Mobile
                blackboard.scrape.course_data(
                    blackboard.get.course_data(
                        # Send Blackboard cookies & course's id
                        request.session["blackboard"], course_id
                    ), course_key, course_id
                )
            )

    # Course's MyUDC details handler
    class Details(APIView):
        """
        Returns course's MyUDC details,
        which includes its location, time, doctor, etc...
        """
        # Returns a single course's details
        @staticmethod
        @login_required("myudc")
        def get(request, course_key, crn, term_code):
            # If crn or term aren't sent
            if not (crn and term_code):
                # Return to API root with an error message
                return APIRoot.get(request, request.path)
            # Otherwise, return requested course's details
            return Response(
                # Get & scrape course's details from MyUDC
                myudc.scrape.course(
                    myudc.get.course(
                        # Send MyUDC session
                        request.session["myudc"],
                        # Send course's key, crn and term code
                        crn, course_key, term_code
                    )
                )
            )

    # Course's Blackboard document download handler
    class Documents(APIView):
        # Returns a course's document file
        @staticmethod
        @login_required("blackboard")
        def get(request, document_id):
            # Get course document data and name from Blackboard
            file_data, file_name = blackboard.get.course_document(
                # Send Blackboard cookies, and document content id and xid
                request.session["blackboard"], *document_id.split("_")
            )
            # Construct a response with document content and type
            response = HttpResponse(**file_data)
            # Specify document file name in response and return it
            response["Content-Disposition"] = f'attachment; filename="{file_name}"'
            return response

        # Course's Blackboard documents download as a zip handler
        class Zip(APIView):
            # Returns a course's documents in a zip file
            @staticmethod
            @login_required("blackboard")
            def get(request, documents_ids, zip_name):
                # Create an HTTP response with content type zip
                response = HttpResponse(content_type="application/x-zip-compressed")
                # Specify zip file name in response
                response["Content-Disposition"] = f'attachment; filename="{zip_name or "documents"}.zip"'
                # Open a zip file that'll contain downloaded documents
                zip_file = ZipFile(response, mode="w")

                # Downloads and adds document to zip file
                def download_document(document_id):
                    # Get course document data and name from Blackboard
                    file_data, file_name = blackboard.get.course_document(
                        # Send Blackboard cookies, and document content id and xid
                        request.session["blackboard"], *document_id.split("_")
                    )
                    # Write downloaded document to zip file
                    zip_file.writestr(file_name, file_data["content"])
                # Create a threads queue
                threads = []
                # Loop through requested documents ids
                for document_id in documents_ids.split(","):
                    # Append a new thread to queue that downloads and zips document
                    threads.append(Thread(target=download_document, args=(document_id,)))
                    # Start created thread
                    threads[-1].start()
                # Join all started threads to main one
                [thread.join() for thread in threads]
                # Once done, close zip file and return it
                zip_file.close()
                return response
