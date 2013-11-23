from django.forms import ModelForm, CharField

from core.models import Payment


class PaymentForm(ModelForm):
    class Meta(object):
        model = Payment

    tags = CharField()  # Resets widget to the default.
