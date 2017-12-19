""" UOSHUB URL Configuration """

from django.conf.urls import url, include
from django.shortcuts import redirect
from django.contrib import admin

urlpatterns = [
    # When browser requests /favicon.ico, redirect to it"s location in /static/img
    url(r"^favicon\.ico$", lambda request: redirect("/static/img/favicon.ico")),
    # If any URL is requested without a trailing slash, redirect to add it
    url("[^/]$", lambda request: redirect(request.path + "/")),
    # /admin/ links to Django"s built-in admin app
    url(r"^admin/", admin.site.urls),
    # /api/ is the RESTful API of UOS HUB
    url(r"^api/", include("API.urls")),
    # Everything else should link to the front-end
    url(r"^", include("Website.urls")),
]
