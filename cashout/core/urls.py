from django.conf.urls import patterns, url

from core import views as core_views


urlpatterns = patterns(
    "",
    url(r"^$", core_views.index, name="core.index"),
    url(r"^list/$", core_views.list, name="core.list"),
)
