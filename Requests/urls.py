from django.conf.urls import url
from .views import *

urlpatterns = [
    # Login path
    url(r"^login/$", Login.as_view()),
    # Layout details path
    url(r"^details/$", LayoutDetails.as_view()),
    # Blackboard updates path
    url(r"^updates/((?P<update>[0-9]{8})/)?$", Updates.as_view()),
    # Terms path (Blackboard and MyUDC)
    # /api/terms returns a list of registered terms
    url(r"^terms/$", Terms.as_view()),
    # /api/terms/<term> returns specified term's MyUDC Details
    url(r"^terms/(?P<term>[0-9]{6})/$", Terms.Details.as_view()),
    # /api/terms/(content or courses) returns specified term's Blackboard content or list of courses
    url(r"^terms/(?P<term>[0-9]{6})/(?P<data_type>deadlines|documents|content|courses)/$", Terms.Content.as_view()),
    # /api/grades/<term> returns specified term's Blackboard courses grades
    url(r"^grades/((?P<term>[0-9]{6})/)?$", Grades.as_view()),
    # Courses path (Blackboard and MyUDC)
    # /api/courses returns a list of registered courses categorized by their terms
    url(r"^courses/$", Courses.as_view()),
    # /api/courses/<Blackboard id> returns course's documents and deadlines
    url(r"^courses/(?P<key>[0-9]{7})/((?P<course>[0-9]{5})/)?$", Courses.Content.as_view()),
    # /api/courses/<MyUDC key>/<CRN>/<term code> returns course's details from MyUDC
    url(r"^courses/(?P<key>[0-9]{7})/(?P<crn>[0-9]{5})/((?P<term>[0-9]{6})/)?$", Courses.Details.as_view()),
    # Outlook emails path
    # /api/emails returns a list of available emails categories
    # /api/emails/<category> returns 20 of specified category's emails
    # /api/emails/<category>/<count> returns <count> of specified category's emails
    url(r"^emails/((?P<category>personal|courses|events)/((?P<count>[0-9]{1,3})/)?)?$", Emails.as_view()),
    # /api/emails/<message id> returns a single email's HTML body content
    url(r"^emails/(?P<message_id>[\w-]+=)/$", Emails.Body.as_view()),
    # Homepage's calendar path
    # /api/calendar returns a list of terms available in academic calendar
    # /api/calendar/<term> returns specified term's calendar events
    url(r"^calendar/((?P<term>[0-9]+)/)?$", Calendar.as_view()),
    # MyUDC holds path
    url(r"^holds/$", Holds.as_view()),
    # Refresh data path
    url(r"^refresh/((?P<date>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)/)?$", Refresh.as_view()),
    # API root path
    url(r"^(.*)", APIRoot.as_view()),
]
