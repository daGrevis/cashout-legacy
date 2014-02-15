from django.conf import settings
from django.core import exceptions as django_exceptions


def filter_by_keys(dict, allowed_keys):
    return {key: dict[key] for key in allowed_keys}


def check_for_csrf_token(request, csrf_token):
    if settings.TESTING:
        return
    if request.COOKIES[settings.CSRF_COOKIE_NAME] != csrf_token:
        raise django_exceptions.SuspiciousOperation()
