"""Django settings. Everything that differs between your computer and SPARC Cloud comes from environment
variables (SPARC Cloud: the app's Settings & secrets tab; DATABASE_URL comes from the attached database)."""
import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env_list(name: str, default: str) -> list[str]:
    return [x.strip() for x in os.environ.get(name, default).split(",") if x.strip()]


DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"   # NEVER 1 on SPARC Cloud

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("DJANGO_SECRET_KEY is not set (SPARC Cloud generates it from sparc.json).")
    SECRET_KEY = "insecure-only-for-your-computer"

# Which host names this site answers to. SPARC Cloud apps are <app>.<startup>.sparc.internal (office/VPN) and
# <app>.<startup>.hosting.sparcinnovations.africa (internet). Health checks bypass this (mysite/health.py).
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS",
                         ".sparc.internal,.hosting.sparcinnovations.africa,localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "https://*.sparc.internal,https://*.hosting.sparcinnovations.africa,"
    "https://*.hosting.sparcinnovations.africa:21443")
# SPARC Cloud adds HTTPS in front of the app and says so in this header.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = not DEBUG

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages",
]

MIDDLEWARE = [
    "mysite.health.HealthCheckMiddleware",          # FIRST: /healthz answers before the host check
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",    # serves /static/ files (CSS of the admin etc.)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"
WSGI_APPLICATION = "mysite.wsgi.application"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

# The database: DATABASE_URL (postgresql://...). For your computer, see README ("Run it on your computer").
if not os.environ.get("DATABASE_URL"):
    raise ImproperlyConfigured("DATABASE_URL is not set: attach a database to the app (Database tab).")
DATABASES = {"default": dj_database_url.config(conn_max_age=60, conn_health_checks=True)}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en"
TIME_ZONE = os.environ.get("TZ", "Africa/Blantyre")
USE_I18N = True
USE_TZ = True

# Static files: collected at start into a folder the app may write (the app runs as user 1000, not root),
# served by WhiteNoise.
STATIC_URL = "static/"
STATIC_ROOT = Path(os.environ.get("DJANGO_STATIC_ROOT", "/tmp/django-static"))
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logs to the screen (= the Logs tab).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
