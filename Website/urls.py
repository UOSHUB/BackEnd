from django.conf.urls import url
from . import views

urlpatterns = [
    # Requesting a static file from the root url links to views.static_files
    url(r'^(?P<filename>.+\.(html|css|js|png|jpg|svg|ico))$', views.static_files),
    # All other requests link to views.layout when the website is open for the first time
    url(r'', views.layout),
]
