from django.conf.urls import patterns, include, url

from core import urls as core_urls


urlpatterns = patterns(
    "",
    url(r"^", include(core_urls)),
)
