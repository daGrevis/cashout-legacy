from datetime import datetime
import calendar

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


def get_balace():
    balance = Payment.objects.aggregate(models.Sum("price"))["price__sum"]
    return balance or 0


def get_available_for_burndown_graph(start_balance):
    now = datetime.now()
    _, days_in_month = calendar.monthrange(now.year, now.month)
    days = range(1, days_in_month + 1)
    day_balance = start_balance / days_in_month
    data = []
    for day in days:
        data.append({
            "x": calendar.timegm(datetime(year=now.year,
                                          month=now.month,
                                          day=day).utctimetuple()),
            "y": round(day_balance * (days_in_month - day), 2),
        })
    return data
