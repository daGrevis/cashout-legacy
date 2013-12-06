from django.forms import ModelForm

from core.models import Payment


class IndexForm(ModelForm):
    class Meta(object):
        model = Payment
        fields = (
            "price",
            "title",
            "tags",
        )


class PaymentForm(ModelForm):
    class Meta(object):
        model = Payment
        fields = (
            "title",
            "description",
            "price",
            "tags",
            "created",
        )
