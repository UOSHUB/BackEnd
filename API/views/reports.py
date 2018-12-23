from rest_framework.response import Response
from rest_framework.views import APIView
from Requests.myudc.reports import get as reports
from Requests import term_code as default_term

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
    def get(request, report_type, term_code):
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
        reports._format = "html"
        term = term_code or default_term
        # Get report and create response
        return Response(
            # Get report from MyUDC using sent term code or the default one otherwise
            getattr(reports, report_type)(request.session["sid"], term)
        )
