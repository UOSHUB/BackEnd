""" WSGI config for UOSHUB project. """

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UOSHUB.settings")

application = get_wsgi_application()
