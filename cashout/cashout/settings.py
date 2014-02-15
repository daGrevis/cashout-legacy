import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "x" * 32

DEBUG = True

TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",

    "south",
    "bootstrapform",
    "taggit",
    "activelink",
    "django_filters",

    "core",
)

ROOT_URLCONF = "cashout.urls"

WSGI_APPLICATION = "cashout.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "database.sqlite3"),
    }
}

LANGUAGE_CODE = "en-us"

USE_TZ = False

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "/static/"

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "core.context_processors.settings",
)

CASHOUT_VERSION = (0, 0, 7)

PER_PAGE = 5

CURRENCIES = (
    "EUR",
    "USD",
    "LVL",
)

DEFAULT_CURRENCY = "EUR"
SECONDARY_CURRENCY = "LVL"

DJANGO_MESSAGES_TO_BOOTSTRAP_ALERTS = {
    "debug": "info",
    "error": "danger",
}

CURRECY_CONVERTOR_MAX_ATTEMPTS = 3

DEFAULT_TITLE_FOR_BALANCE_RESET = "Balance reset"
DEFAULT_TAGS_FOR_BALANCE_RESET = (
    "balance reset",
)

TESTING = "test" in sys.argv
