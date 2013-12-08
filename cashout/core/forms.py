from django import forms

from core.models import Payment


class IndexForm(forms.ModelForm):
    class Meta(object):
        model = Payment
        fields = (
            "title",
            "price",
            "tags",
        )


class PaymentForm(forms.ModelForm):
    class Meta(object):
        model = Payment
        fields = (
            "title",
            "description",
            "price",
            "tags",
            "created",
        )
