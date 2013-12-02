from datetime import datetime
import calendar

from arrow import Arrow

from taggit.managers import TaggableManager

from django.db import models
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField)


class Payment(models.Model):
    tags = TaggableManager()

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(default=None, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __unicode__(self):
        return u"title: {}, price: {}".format(self.title, self.price)

    @staticmethod
    def get_balance(queryset):
        balance = queryset.aggregate(models.Sum("price"))["price__sum"]
        return balance or 0

    def is_income(self):
        return self.price > 0

    def is_expense(self):
        return self.price < 0


def get_count_of_days_in_month(year, month):
    _, days_in_month = calendar.monthrange(year, month)
    return days_in_month


def get_ideal_for_burndown_graph(start_balance):
    now = datetime.now()
    count_of_days_in_month = get_count_of_days_in_month(now.year, now.month)
    days = range(1, count_of_days_in_month + 1)
    day_balance = start_balance / count_of_days_in_month
    data = []
    for day in days:
        data.append({
            "x": (Arrow(year=now.year, month=now.month, day=day)).timestamp,
            "y": round(day_balance * (count_of_days_in_month - day), 2),
        })
    return data


def get_actual_for_burndown_graph(start_balance, payments):
    now = datetime.now()
    days = range(1, get_count_of_days_in_month(now.year, now.month) + 1)
    data = []
    balance = start_balance
    for day in days:
        payments_in_day = []
        for payment in payments:
            if (payment.created).day == day:
                payments_in_day.append(payment)
        spent_in_day = sum([payment.price for payment in payments_in_day])
        balance += spent_in_day
        data.append({
            "x": (Arrow(year=now.year, month=now.month, day=day)).timestamp,
            "y": round(balance, 2),
        })
    return data
