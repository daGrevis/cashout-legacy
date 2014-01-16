from datetime import datetime
import json
from collections import OrderedDict

from jsonview.decorators import json_view

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib import messages

from core.models import (Payment, get_data_for_burndown_graph,
                         get_data_for_frequency_graph, CurrencyConverter)
from core.forms import IndexForm, PaymentForm, BalanceResetForm
from core.filters import PaymentFilter


def index(request):
    if request.method == "POST":
        payment_form = IndexForm(request.POST)
        if payment_form.is_valid():
            payment_form.save()
            messages.success(request, "Payment was successfully added!")
            return redirect("core.index")
    else:
        payment_form = IndexForm()
    balance = Payment.get_price(Payment.objects)
    balance_in_secondary_currency = None
    if settings.SECONDARY_CURRENCY:
        balance_in_secondary_currency = (CurrencyConverter().get_price(balance,
                                         settings.DEFAULT_CURRENCY,
                                         settings.SECONDARY_CURRENCY))
    return render(request, "index.html", {
        "payment_form": payment_form,
        "balance": balance,
        "balance_in_secondary_currency": balance_in_secondary_currency,
    })


def payment_list(request):
    payment_filter = PaymentFilter(request.GET, queryset=Payment.objects)
    payment_paginator = Paginator(payment_filter.qs, settings.PER_PAGE)
    page = request.GET.get("page")
    try:
        payments = payment_paginator.page(page)
    except PageNotAnInteger:
        payments = payment_paginator.page(1)
    except EmptyPage:
        payments = payment_paginator.page(payment_paginator.num_pages)
    if not payments:
        messages.warning(request, "No payments were found!")
    return render(request, "payment_list.html", {
        "payment_filter": payment_filter,
        "payment_paginator": payment_paginator,
        "payments": payments,
    })


def payment_item(request, payment_pk):
    payment = get_object_or_404(Payment, pk=payment_pk)
    if "delete" in request.GET:
        payment.delete()
        messages.success(request, "Payment was successfully deleted!")
        return redirect("core.payment_list")
    if request.method == "POST":
        payment_form = PaymentForm(request.POST, instance=payment)
        if payment_form.is_valid():
            payment_form.save()
            messages.success(request, "Payment was successfully updated!")
            return redirect("core.payment_item", payment_pk=payment_pk)
    else:
        payment_form = PaymentForm(instance=payment)
    return render(request, "payment_item.html", {
        "payment_form": payment_form,
        "payment_pk": payment.pk,
    })


@json_view
def payment_tags(request):
    query = (request.GET).get("query")
    tags = Payment.tags.most_common()
    if query:
        tags = tags.filter(name__icontains=query)
    # TODO: A bug? https://github.com/alex/django-taggit/issues/173
    tags = [name for name, _ in tags.values_list("name", "num_times")]
    return {"tags": tags}


@json_view
def payment_titles(request):
    query = (request.GET).get("query")
    title_qs = Payment.objects.order_by("-created")
    if query:
        title_qs = title_qs.filter(title__icontains=query)
    titles = list((title_qs.values_list("title", flat=True)))
    # Removes duplicates. Can't use sets here because order is important.
    titles = list(OrderedDict.fromkeys(titles))
    return {"titles": titles}


@json_view
def payment_guess(request):
    """Tries to guess payment by it's title and returns price and tags."""
    if "title" not in request.GET:
        return None
    title = request.GET["title"]
    payments = Payment.objects.filter(title=title).order_by("-created")
    try:
        payment = payments[0]
    except IndexError:
        # No match.
        return None
    price = round(payment.price, 2)
    tags = list(payment.tags.all().values_list("name", flat=True))
    return {"price": price, "tags": tags}


def burndown_graph(request):
    payments = Payment.objects.filter(created__month=(datetime.now()).month)
    graph_data = get_data_for_burndown_graph(payments)
    graph_data = json.dumps(graph_data)
    return render(request, "burndown_graph.html", {
        "graph_data": graph_data,
    })


def frequency_graph(request):
    graph_data = get_data_for_frequency_graph()
    graph_data = json.dumps(graph_data)
    return render(request, "frequency_graph.html", {
        "graph_data": graph_data,
    })


def balance_reset(request):
    balance = Payment.get_price(Payment.objects)
    balance_in_secondary_currency = None
    if settings.SECONDARY_CURRENCY:
        balance_in_secondary_currency = (CurrencyConverter().get_price(balance,
                                         settings.DEFAULT_CURRENCY,
                                         settings.SECONDARY_CURRENCY))
    if request.method == "POST":
        balance_reset_form = BalanceResetForm(request.POST)
        if balance_reset_form.is_valid():
            payment = Payment()
            payment.title = settings.DEFAULT_TITLE_FOR_BALANCE_RESET
            payment.currency = settings.DEFAULT_CURRENCY
            payment.price = balance - balance_reset_form.cleaned_data["price"]
            payment.price *= -1
            payment.save()
            payment.tags.add(*settings.DEFAULT_TAGS_FOR_BALANCE_RESET)
            messages.success(request, "Balance was successfully reset!")
            return redirect("core.index")
    else:
        balance_reset_form = BalanceResetForm()
    return render(request, "balance_reset.html", {
        "balance": balance,
        "balance_in_secondary_currency": balance_in_secondary_currency,
        "balance_reset_form": balance_reset_form,
    })
