from django import forms
from django.conf import settings

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
            "currency",
            "tags",
            "created",
        )


class BalanceResetForm(forms.Form):
    price = forms.DecimalField(max_digits=9, decimal_places=2)
