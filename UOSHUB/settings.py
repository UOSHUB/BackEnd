""" Django settings for UOSHUB project. """

import os
import netifaces

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use SECRET_KEY from current machine"s environment, otherwise use this one below
SECRET_KEY = os.environ.get("SECRET_KEY", "ue3axgr(ny2a027!bb2_exy#040)$vbq8q04(ogs80p76m**2d")

# Use DEBUG from current machine"s environment, otherwise set it to True
DEBUG = os.environ.get("DEBUG") != "False"

# Add machine's IP address to Django"s allowed hosts
# This is necessary because otherwise Gunicorn will reject the connections
ALLOWED_HOSTS = [".uoshub.com"]
for interface in netifaces.interfaces():
    addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in addrs:
        ALLOWED_HOSTS.append(addrs[netifaces.AF_INET][0]["addr"])

# Installed applications
INSTALLED_APPS = [
    # UOS HUB applications
    "API.apps.APIConfig",
    "Website.apps.WebsiteConfig",
    # Django Admin app and its dependencies
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "compressor"
]

# Used middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Django compressor configurations
COMPRESS_ENABLED = True
COMPRESS_OUTPUT_DIR = "min"
COMPRESS_ROOT = os.path.join(BASE_DIR, "Website/static/")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# In development
if DEBUG:
    # Combine static files without compression
    COMPRESS_JS_FILTERS = []
else:  # In production
    # Enable offline compression
    COMPRESS_OFFLINE = True
    COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.rCSSMinFilter"]
    COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.SlimItFilter"]
    # Secure session cookies
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# Configure Django to use cookie based sessions
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Configure Django templates (only for /admin/ pages)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [COMPRESS_ROOT],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Setup URLs for the WSGI application and project root
WSGI_APPLICATION = "UOSHUB.wsgi.application"
ROOT_URLCONF = "UOSHUB.urls"

# SQLite Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Internationalization
TIME_ZONE = "Asia/Dubai"
USE_I18N = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"

# This is necessary so that Nginx can handle requests for static files
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
