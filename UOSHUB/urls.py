""" UOSHUB URL Configuration """

from django.conf.urls import url, include
from django.shortcuts import redirect
from django.contrib import admin

urlpatterns = [
    # /admin/ links to Django"s built-in admin app
    url(r"^admin/", admin.site.urls),
    # /api/ is the RESTful api for the Requests logic
    url(r"^api/", include("Requests.urls")),
    # If /admin or /api are requested without a trailing slash, redirect to add it
    url(r"^(?:admin|api)$", lambda request: redirect(request.path + "/")),
    # Everything else should link to the front-end
    url(r"^", include("Website.urls")),
]
