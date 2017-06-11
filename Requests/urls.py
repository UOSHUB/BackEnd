from django.conf.urls import url
from .views import *

urlpatterns = [
    # Placeholder for api root path
    url(r'^$', index, name='index')
]
