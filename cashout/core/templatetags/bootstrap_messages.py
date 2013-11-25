from django import template
from django.conf import settings


register = template.Library()


@register.filter
def bootstrap_messages(value):
    try:
        return settings.DJANGO_MESSAGES_TO_BOOTSTRAP_ALERTS[value]
    except KeyError:
        return value
