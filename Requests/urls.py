from django.conf.urls import url
from .views import *

urlpatterns = [
    # API root path
    url(r'^$', APIRoot.as_view()),
    # Login path
    url(r'^login/?$', Login.as_view()),
    # Core details path
    url(r'^details/?$', CoreDetails.as_view()),
]
