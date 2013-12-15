import django_filters

from core.models import Payment


class PaymentFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_type="icontains")

    class Meta(object):
        model = Payment
        fields = (
            "title",
        )
        order_by = (
            "-created",
            "price",
            "-price",
        )
