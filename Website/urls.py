from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<filename>.+\.(html|css|js|png|jpg|svg))$', views.static_files),
    url(r'', views.layout),
]
