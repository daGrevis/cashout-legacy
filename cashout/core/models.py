from datetime import datetime
import calendar
import json
from decimal import Decimal
from collections import Counter

from arrow import Arrow
import requests
from taggit.managers import TaggableManager
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField)

from django.db import models
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)


class PaymentQS(models.query.QuerySet):
    def incomes(self):
        return self.filter(price__gt=0)

    def expenses(self):
        return self.filter(price__lt=0)


class PaymentManager(models.Manager):
    def get_queryset(self):
        return PaymentQS(self.model)


class Payment(models.Model):
    _cache_for_currency_converter = None

    CURRENCY_CHOICES = [(currency, currency) for currency
                        in settings.CURRENCIES]

    objects = PaymentManager()
    tags = TaggableManager()

    created = CreationDateTimeField(editable=True)
    modified = ModificationDateTimeField()
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(default="", blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    currency = (models.CharField(max_length=3,
                choices=CURRENCY_CHOICES, default=settings.DEFAULT_CURRENCY))
    category = models.ForeignKey(Category, null=True)

    def __unicode__(self):
        return u"title: {}, price: {}".format(self.title, self.price)

    @staticmethod
    def get_price(queryset):
        payments = queryset.all()
        price = Decimal(0)
        currency_converter = CurrencyConverter()
        for payment in payments:
            price += currency_converter.get_price(payment.price,
                                                  payment.currency,
                                                  settings.DEFAULT_CURRENCY)
        return price or 0

    def is_income(self):
        return self.price > 0

    def is_expense(self):
        return self.price < 0

    def get_price_in_secondary_currency(self):
        if self.currency == settings.SECONDARY_CURRENCY:
            return self.price
        if self._cache_for_currency_converter is None:
            self._cache_for_currency_converter = CurrencyConverter()
        currency_converter = self._cache_for_currency_converter
        return currency_converter.get_price(self.price,
                                            settings.DEFAULT_CURRENCY,
                                            settings.SECONDARY_CURRENCY)

    def get_tags_as_list(self):
        return list(self.tags.values_list("name", flat=True))


def get_data_for_burndown_chart(payments):
    data = {}
    now = datetime.now()
    _, count_of_days_in_month = calendar.monthrange(now.year, now.month)
    days = range(1, count_of_days_in_month + 1)
    start_balance = Payment.get_price(payments.incomes())
    data["start_balance"] = round(start_balance, 2)
    day_balance = start_balance / count_of_days_in_month
    data["ideal"] = []
    data["actual"] = []
    actual_balance = start_balance
    for day in days:
        timestamp = (Arrow(year=now.year, month=now.month, day=day)).timestamp
        x = timestamp * 1000  # Unix timestamp in milliseconds.
        y = round(day_balance * (count_of_days_in_month - day), 2),
        data["ideal"].append([x, y])
        if day > now.day:
            continue
        # TODO: Code below executes a query on each iteration!
        expenses_today = payments.expenses().filter(created__day=day)
        spent_today = Payment.get_price(expenses_today) * -1
        actual_balance -= spent_today
        data["actual"].append([x, round(actual_balance)])
    return data


def get_data_for_frequency_chart():
    payments = Payment.objects.filter(created__month=
                                      (datetime.now()).month).expenses()
    tags = []
    for payment in payments:
        tags.extend(payment.tags.all().values_list("name", flat=True))
    data = []
    for label, frequency in Counter(tags).most_common(10):
        data.append({"data": [[label, frequency]]})
    return data


class GoogleExchangeBackend(object):
    def get_url(self, currency_from, currency_to):
        url = "http://rate-exchange.appspot.com/currency?from={}&to={}"
        url = url.format(currency_from, currency_to)
        return url

    def parse_data(self, data):
        data = json.loads(data)
        return data


class CurrencyRetrievalError(Exception):
    pass


class CurrencyParsingError(Exception):
    pass


class CurrencyConverter(object):
    cached_currencies = {}

    def __init__(self, backend=GoogleExchangeBackend):
        self.backend = backend()

    def get_rate(self, currency_from, currency_to):
        if currency_from == currency_to:
            return 1
        rate_from_cache = self._get_from_cache(currency_from, currency_to)
        if rate_from_cache:
            return rate_from_cache
        url = (self.backend).get_url(currency_from, currency_to)
        try:
            data = self._request(url)
        except requests.exceptions.RequestException:
            raise CurrencyRetrievalError()
        try:
            data = (self.backend).parse_data(data)
        except ValueError:
            raise CurrencyParsingError()
        rate = Decimal(data["rate"]).quantize(Decimal(".01"))
        self._set_in_cache(currency_from, currency_to, rate)
        return rate

    def get_price(self, price, currency_from, currency_to):
        rate = self.get_rate(currency_from, currency_to)
        return Decimal(price * rate).quantize(Decimal(".01"))

    def _get_from_cache(self, currency_from, currency_to):
        cache_key = (currency_from, currency_to)
        return (self.cached_currencies).get(cache_key)

    def _set_in_cache(self, currency_from, currency_to, rate):
        cache_key = (currency_from, currency_to)
        self.cached_currencies[cache_key] = rate

    def _request(self, url, attempts=0):
        try:
            return (requests.get(url)).content
        except requests.exceptions.RequestException:
            if attempts > settings.CURRECY_CONVERTOR_MAX_ATTEMPTS:
                raise
            return self._request(url, attempts + 1)
