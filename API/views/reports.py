from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from Requests.myudc.reports import get as reports
from Requests import term_code

# Define list of reports types
reports_types = {
    report_type: report_type.lower().replace(" ", "_")
    for report_type in (
        "Unofficial Transcript",
        "Personal Information",
        "Summarized Schedule",
        "Offered Courses",
        "Final Exams",
        "Study Plan"
    )
}

# Student's reports requests handler
class Reports(APIView):
    """
    This loads the six different reports from MyUDC as an HTML page.
    """
    # Returns student's html report on GET request
    @staticmethod
    def get(request, report_type, report_format):
        # If report type is not specified
        if not report_type:
            # Return a list of available report types
            return Response({
                description: request.build_absolute_uri(method + "/")
                for description, method in reports_types.items()
            })
        # If report type is not supported
        if report_type not in reports_types.values():
            # Return 404 report not found error
            return Response("Report not found!", status=404)
        # Set report variables
        reports._format = report_format = report_format or "pdf"
        sid = request.session["sid"]
        # Get report and create response
        response = HttpResponse(
            # Get report from MyUDC
            getattr(reports, report_type)(sid, term_code),
            # Set content type as the sent format
            content_type=f"text/{report_format[:4]}"
        )
        # If report is requested in pdf
        if report_format == "pdf":
            # Set type and download file headers
            response["Content-Type"] = "application/pdf"
            response["Content-Disposition"] = f'filename="{report_type}_{sid}.pdf"'
        return response
