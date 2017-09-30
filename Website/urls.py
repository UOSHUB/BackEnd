from django.conf.urls import url
from . import views

urlpatterns = [
    # All website related requests link to views.layout
    # as the layout loads other dependencies as per request
    url(r'', views.layout),
]
