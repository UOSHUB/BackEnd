from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # When browser requests /favicon.ico, redirect to it"s location in /static/img
    url(r"^favicon\.ico$", RedirectView.as_view(url="/static/img/favicon.ico")),
    # All other requests link to views.layout when the website is open for the first time
    url(r'', views.layout),
]
