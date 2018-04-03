from django.conf.urls import url
from . import views

urlpatterns = [
    # Captures special abbreviations and redirects to UOS websites
    url(r"^(?P<site>bb|udc|ms|uos)/?$", views.redirect_to_uos),
    # All website related requests link to views.layout
    # as the layout loads other dependencies as per request
    url(r"", views.layout),
]
