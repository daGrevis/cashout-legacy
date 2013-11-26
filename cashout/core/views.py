import json

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib import messages

from core.models import Payment, get_balace, get_available_for_burndown_graph
from core.forms import PaymentForm
from core.filters import PaymentFilter


def index(request):
    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment_form.save()
            return redirect("core.index")
    else:
        payment_form = PaymentForm()
    balance = get_balace()
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
    return render(request, "payment_list.html", {
        "payment_filter": payment_filter,
        "payment_paginator": payment_paginator,
        "payments": payments,
    })


def payment_item(request, payment_pk):
    payment = get_object_or_404(Payment, pk=payment_pk)
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
    })


def burndown_graph(request):
    graph_data = {
        "spent": [
            {"x": 1385491640, "y": 20},
            {"x": 1385491640 + 60 * 60 * 8, "y": 40},
            {"x": 1385491640 + 60 * 60 * 24, "y": 75},
        ],
    }
    graph_data["available"] = get_available_for_burndown_graph(100.)
    graph_data = json.dumps(graph_data)
    return render(request, "burndown_graph.html", {
        "graph_data": graph_data,
    })
