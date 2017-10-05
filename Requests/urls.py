from django.conf.urls import url
from .views import *

urlpatterns = [
    # Login path
    url(r"^login/$", Login.as_view()),
    # Layout details path
    url(r"^details/$", LayoutDetails.as_view()),
    # Blackboard updates path
    url(r"^updates/$", Updates.as_view()),
    # MyUDC terms path
    # /api/terms returns a list of registered terms
    # /api/terms/<term> returns specified term's data
    url(r"^schedule/((?P<term>[0-9]+)/)?$", Terms.as_view()),
    # Blackboard Courses path
    # /api/courses returns a list of registered courses categorized by their terms
    url(r"^courses/$", Courses.as_view()),
    # /api/courses/<Blackboard id> returns course's documents and deadlines
    url(r"^courses/(?P<bb>[0-9]{5})/$", Courses.Content.as_view()),
    # /api/courses/<MyUDC key>/<CRN>/<term code> returns course's details from MyUDC
    url(r"^courses/(?P<key>[0-9]{7})/((?P<crn>[0-9]{5})/)?((?P<term>[0-9]{6})/)?$", Courses.Details.as_view()),
    # Outlook emails path
    url(r"^emails/$", Emails.as_view()),
    # Outlook emails previews path
    url(r"^emails/previews/$", Emails.Previews.as_view()),
    # Homepage's calendar path
    # /api/calendar returns a list of terms available in academic calendar
    # /api/schedule/<term> returns specified term's calendar events
    url(r"^calendar/((?P<term>[0-9]+)/)?", Calendar.as_view()),
    # API root path
    url(r"^(.*)", APIRoot.as_view()),
]
