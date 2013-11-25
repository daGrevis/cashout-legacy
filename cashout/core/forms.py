from django.forms import ModelForm

from core.models import Payment


class PaymentForm(ModelForm):
    class Meta(object):
        model = Payment
