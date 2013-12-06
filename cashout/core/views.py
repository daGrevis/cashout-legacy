from datetime import datetime
import json

from jsonview.decorators import json_view

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib import messages

from core.models import (Payment, get_ideal_for_burndown_graph,
                         get_actual_for_burndown_graph)
from core.forms import IndexForm, PaymentForm
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
    balance = Payment.get_balance(Payment.objects)
    return render(request, "index.html", {
        "payment_form": payment_form,
        "balance": balance,
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
def tags(request):
    query = (request.GET).get("query")
    tags = Payment.tags.most_common()
    if query:
        tags = tags.filter(name__icontains=query)
    # TODO: A bug? https://github.com/alex/django-taggit/issues/173
    tags = [name for name, _ in tags.values_list("name", "num_times")]
    tags = list(tags)
    return {"tags": tags}


def burndown_graph(request):
    payments_in_month = Payment.objects.filter(created__month=
                                               (datetime.now()).month)
    start_balance = Payment.get_balance(payments_in_month.filter(price__gt=0))
    ideal = get_ideal_for_burndown_graph(start_balance)
    actual = (get_actual_for_burndown_graph(
              start_balance, payments_in_month.filter(price__lt=0)))
    graph_data = {
        "ideal": ideal,
        "actual": actual,
    }
    graph_data = json.dumps(graph_data)
    return render(request, "burndown_graph.html", {
        "graph_data": graph_data,
    })
