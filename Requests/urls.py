from django.conf.urls import url
from .views import *

urlpatterns = [
    # API root path
    url(r'^$', APIRoot.as_view()),
]
