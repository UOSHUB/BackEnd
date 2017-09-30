from rest_framework.response import Response
from rest_framework.views import APIView
from Requests import calendar


# Academic calendar requests handler
class Calendar(APIView):
    """
    This returns academic calendar events,
    which's an array of events in a specific term
    """
    # Returns term's array events on GET request
    def get(self, request, term=None):
        # If accessing "/calendar/" without specifying term
        if not term:
            # Return all terms in academic calendar
            return Response({
                # Format terms in {term name: term URL} pairs
                name: request.build_absolute_uri(code)
                # Loop through all terms scraped from calendar
                for name, code in calendar.all_terms(
                    # Get academic calendar page
                    calendar.academic_calendar()
                ).items()
            })
        # Return requested term's dictionary of events
        return Response(
            # Scrape term's events
            calendar.term_events(
                # Get academic calendar page
                calendar.academic_calendar(),
                # Send specified term code
                term
            )
        )
