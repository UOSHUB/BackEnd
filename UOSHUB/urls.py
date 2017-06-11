"""UOSHUB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.shortcuts import redirect
from django.contrib import admin

urlpatterns = [
    # /admin/ links to Django's built-in admin app
    url(r'^admin/', admin.site.urls),
    # /api/ is the RESTful api for the Requests logic
    url(r'^api/', include('Requests.urls')),
    # If /admin or /api are requested without a trailing slash, redirect to add it
    url(r'^(?:admin|api)$', lambda request: redirect(request.path + '/')),
    # Everything else should link to the front-end
    url(r'^', include('Website.urls')),
]
