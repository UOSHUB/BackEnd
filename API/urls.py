from django.conf.urls import url
from .views import *

urlpatterns = [
    # Login path
    url(r"^login/$", Login.as_view()),
    # Layout details path
    url(r"^details/$", LayoutDetails.as_view()),
    # Blackboard updates path
    url(r"^updates/((?P<update_id>[0-9]{8})/)?$", Updates.as_view()),
    # Terms path (Blackboard and MyUDC)
    # /api/terms returns a list of registered terms
    url(r"^terms/$", Terms.as_view()),
    # /api/terms/<term> returns specified term's MyUDC Details
    url(r"^terms/(?P<term_code>[0-9]{6})/$", Terms.Details.as_view()),
    # /api/terms/(content or courses) returns specified term's Blackboard content or list of courses
    url(r"^terms/(?P<term_code>[0-9]{6})/(?P<data_type>deadlines|documents|content|courses)/$", Terms.Content.as_view()),
    # /api/grades/<term> returns specified term's Blackboard courses grades
    url(r"^grades/((?P<term_code>[0-9]{6})/)?$", Grades.as_view()),
    # Courses path (Blackboard and MyUDC)
    # /api/courses returns a list of registered courses categorized by their terms
    url(r"^courses/$", Courses.as_view()),
    # /api/courses/<MyUDC key>/<Blackboard id> returns course's documents and deadlines
    url(r"^courses/(?P<course_key>[0-9]{7})/((?P<course_id>[0-9]{5})/)?$", Courses.Content.as_view()),
    # /api/courses/<MyUDC key>/<CRN>/<term> returns course's details from MyUDC
    url(r"^courses/(?P<course_key>[0-9]{7})/(?P<crn>[0-9]{5})/((?P<term_code>[0-9]{6})/)?$", Courses.Details.as_view()),
    # /api/documents/<document id> returns a course's document file from Blackboard
    url(r"^documents/(?P<document_id>[0-9]+_[0-9]+)/$", Courses.Documents.as_view()),
    # /api/documents/zip/<documents ids>/<zip name> returns a course's documents in a zip file from Blackboard
    url(r"^documents/zip/(?P<documents_ids>[0-9]+_[0-9]+(?:,[0-9]+_[0-9]+)*)/((?P<zip_name>.+)/)?$", Courses.Documents.Zip.as_view()),
    # Outlook emails path
    # /api/emails returns a list of available emails categories
    # /api/emails/<category> returns 20 of specified category's emails
    # /api/emails/<category>/<count> returns <count> of specified category's emails
    url(r"^emails/((?P<category>personal|courses|events)/((?P<count>[0-9]{1,3})/)?)?$", Emails.as_view()),
    url(r"^emails/send/$", Emails.Send.as_view()),
    # /api/emails/<message id> returns a single email's HTML body content
    url(r"^emails/(?P<message_id>[\w-]+=)/$", Emails.Body.as_view()),
    # /api/emails/<message id>/<attachment id> returns a single email's decoded attachment
    url(r"^emails/(?P<message_id>[\w-]+=)/(?P<attachment_id>[\w-]+=)/$", Emails.Attachment.as_view()),
    # Homepage calendar path
    # /api/calendar returns a list of terms available in academic calendar
    # /api/calendar/<term> returns specified term's calendar events
    url(r"^calendar/((?P<term_code>[0-9]{6})/)?$", Calendar.as_view()),
    # MyUDC final exams path
    # /api/finals returns a list of terms that could have finals
    # /api/finals/<term> returns specified term's final exams
    url(r"^finals/((?P<term_code>[0-9]{6})/)?$", Finals.as_view()),
    # MyUDC holds path
    url(r"^holds/$", Holds.as_view()),
    # Design Schedule path (MyUDC and its Reports)
    # /api/design returns a list of registrable courses
    # url(r"^design/(?P<term_code>[0-9]{6})/$", Design.as_view()),
    # Services subscription path
    url(r"^subscribe/$", Subscribe.as_view()),
    # Blackboard assignment submission path
    url(r"^submit/(?P<course_id>[0-9]{5})/(?P<content_id>[0-9]{7})/$", Submit.as_view()),
    # Refresh data path
    url(r"^refresh/((?P<date>\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)/)?$", Refresh.as_view()),
    # API root path
    url(r"^(.*)", APIRoot.as_view()),
]
