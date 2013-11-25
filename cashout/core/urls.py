from django.conf.urls import patterns, url

from core import views as core_views


urlpatterns = patterns(
    "",
    url(r"^$", core_views.index, name="core.index"),
    url(r"^payments/$", core_views.payment_list, name="core.payment_list"),
    url(r"^payments/(?P<payment_pk>\d+)/$", core_views.payment_item, name="core.payment_item"),
)
