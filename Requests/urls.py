from django.conf.urls import url
from .views import *

urlpatterns = [
    # API root path
    url(r'^$', APIRoot.as_view()),
    # Login path
    url(r'^login/?$', Login.as_view()),
    # Layout details path
    url(r'^details/?$', LayoutDetails.as_view()),
    # Schedule dictionary path
    url(r'^schedule/?$', Schedule.as_view()),
]
