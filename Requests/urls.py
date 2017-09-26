from django.conf.urls import url
from .views import *

urlpatterns = [
    # API root path
    url(r"^$", APIRoot.as_view()),
    # Login path
    url(r"^login/?$", Login.as_view()),
    # Layout details path
    url(r"^details/?$", LayoutDetails.as_view()),
    # Blackboard updates path
    url(r"^updates/?$", Updates.as_view()),
    # Schedule dictionary path (by term code)
    url(r"^schedule(/((?P<term>[0-9]+)/?)?)?$", Schedule.as_view()),
    # Courses path
    url(r"^courses/?$", Courses.as_view()),
    # Emails path
    url(r"^emails/?$", Emails.as_view()),
    # Emails previews path
    url(r"^emails/previews/?$", Emails.Previews.as_view()),
]
