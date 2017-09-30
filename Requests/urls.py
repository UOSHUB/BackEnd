from django.conf.urls import url
from .views import *

urlpatterns = [
    # Login path
    url(r"^login/$", Login.as_view()),
    # Layout details path
    url(r"^details/$", LayoutDetails.as_view()),
    # Blackboard updates path
    url(r"^updates/$", Updates.as_view()),
    # MyUDC schedule path
    # /api/schedule returns a list of registered terms
    # /api/schedule/<term> returns specified term's schedule
    url(r"^schedule/((?P<term>[0-9]+)/)?$", Schedule.as_view()),
    # Blackboard Courses path
    # /api/courses returns a list of registered courses categorized by their terms
    # /api/courses/<course or term> returns course's or term's documents and deadlines
    # /api/courses/<course or term>/<"documents" or "deadlines"> returns course's or term's documents or deadlines
    url(r"^courses/(((?P<course>[0-9]+)|in(/(?P<term>[0-9]+))?)/((?P<data_type>[\w]+)/)?)?$", Courses.as_view()),
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
