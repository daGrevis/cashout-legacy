from datetime import datetime
import calendar

from arrow import Arrow

from taggit.managers import TaggableManager

from django.db import models
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField)


class PaymentQS(models.query.QuerySet):
    def incomes(self):
        return self.filter(price__gt=0)

    def expenses(self):
        return self.filter(price__lt=0)


class PaymentManager(models.Manager):
    def get_queryset(self):
        return PaymentQS(self.model)


class Payment(models.Model):
    objects = PaymentManager()
    tags = TaggableManager()

    created = CreationDateTimeField(editable=True)
    modified = ModificationDateTimeField()
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(default="", blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __unicode__(self):
        return u"title: {}, price: {}".format(self.title, self.price)

    @staticmethod
    def get_price(queryset):
        price = queryset.aggregate(models.Sum("price"))["price__sum"]
        return price or 0

    def is_income(self):
        return self.price > 0

    def is_expense(self):
        return self.price < 0


def get_data_for_burndown_graph(payments):
    now = datetime.now()
    _, count_of_days_in_month = calendar.monthrange(now.year, now.month)
    days = range(1, count_of_days_in_month + 1)
    start_balance = Payment.get_price(payments.incomes())
    day_balance = start_balance / count_of_days_in_month
    data = {
        "ideal": [],
        "actual": [],
    }
    actual_balance = start_balance
    for day in days:
        timestamp = (Arrow(year=now.year, month=now.month, day=day)).timestamp
        data["ideal"].append({
            "x": timestamp,
            "y": round(day_balance * (count_of_days_in_month - day), 2),
        })
        if day > now.day:
            continue
        # TODO: Code below executes a query on each iteration!
        expenses_today = payments.expenses().filter(created__day=day)
        spent_today = Payment.get_price(expenses_today) * -1
        actual_balance -= spent_today
        data["actual"].append({
            "x": timestamp,
            "y": round(actual_balance, 2),
        })
    return data
