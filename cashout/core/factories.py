import random

from faker import Factory
from factory.django import DjangoModelFactory

from django.conf import settings

from core.models import Payment, Category


fake_factory = Factory.create()


def fake_price():
    return fake_factory.pydecimal(left_digits=random.randint(1, 7),
                                  right_digits=2)


def fake_tags():
    return list(set(fake_factory.words()))  # Unique.


def fake_iso8601_without_t():
    iso8601 = fake_factory.iso8601()
    iso8601_without_t = iso8601.replace("T", " ")
    return iso8601_without_t


class PaymentFactory(DjangoModelFactory):
    FACTORY_FOR = Payment

    title = fake_factory.word()
    description = fake_factory.sentence()
    price = fake_price()
    currency = settings.DEFAULT_CURRENCY
    created = fake_iso8601_without_t()


class CategoryFactory(DjangoModelFactory):
    FACTORY_FOR = Category

    title = fake_factory.word()
