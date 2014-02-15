from django.conf.urls import patterns, url

from core import views as core_views


urlpatterns = patterns(
    "",
    url(
        r"^$",
        core_views.index,
        name="core.index",
    ),
    url(
        r"^payments/$",
        core_views.payment_list,
        name="core.payment_list",
    ),
    url(
        r"^payments/(?P<payment_pk>\d+)/$",
        core_views.payment_item,
        name="core.payment_item",
    ),
    url(
        r"^payment_tags/$",
        core_views.payment_tags,
        name="core.payment_tags",
    ),
    url(
        r"^payment_titles/$",
        core_views.payment_titles,
        name="core.payment_titles",
    ),
    url(
        r"^payment_guess/$",
        core_views.payment_guess,
        name="core.payment_guess",
    ),
    url(
        r"^charts/burndown/$",
        core_views.burndown_chart,
        name="core.burndown_chart",
    ),
    url(
        r"^charts/frequency/$",
        core_views.frequency_chart,
        name="core.frequency_chart",
    ),
    url(
        r"^charts/expenses/$",
        core_views.expenses_chart,
        name="core.expenses_chart",
    ),
    url(
        r"^balance_reset/$",
        core_views.balance_reset,
        name="core.balance_reset",
    ),
)
