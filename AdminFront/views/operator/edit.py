# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import pytz
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from AdminFront.forms import ClientForm, CommercialForm, BookingPartenerForm
from Back_Source.models import Commercial, BookingPartner
from Back_Source.models import VehicleModel, Client, Airport, Operator


def client_edit(request, pk):
    if not request.user.is_authenticated():
        raise Http404("Page non trouvé")

    if request.method == "POST":
        form = ClientForm(request.POST, instance=Client.objects.get(id=pk))
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = Operator.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/operator/manager/')
    else:
        form = ClientForm(instance=Client.objects.get(id=pk))
    if request.user.is_superuser or Operator.objects.filter(user=request.user).exists():
        return render(request, 'operator/object_edit.html',
                      {"sections": ["Gestion", "Edition Client", str(pk)],
                       "form": form, "title": "Clients", "active": 3,
                       "sub_active": 1})
    else:
        return redirect('/')


def commercial_edit(request, pk):
    if not request.user.is_authenticated():
        raise Http404("Page non trouvé")

    if request.method == "POST":
        form = CommercialForm(request.POST, instance=Commercial.objects.get(id=pk))
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = Operator.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/operator/manager/')
    else:
        form = CommercialForm(instance=Commercial.objects.get(id=pk))
    if request.user.is_superuser or Operator.objects.filter(user=request.user).exists():
        return render(request, 'operator/object_edit.html',
                      {"sections": ["Gestion", "Edition Commerciaux", str(pk)],
                       "form": form, "title": "Commerciaux", "active": 3,
                       "sub_active": 1})
    else:
        return redirect('/')


def booking_edit(request, pk):
    if not request.user.is_authenticated():
        raise Http404("Page non trouvé")

    if request.method == "POST":
        form = BookingPartenerForm(request.POST, instance=BookingPartner.objects.get(id=pk))
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = Operator.objects.filter(user=request.user)[0]

            date = request.POST.get('date', None)
            time = request.POST.get('time', None)

            raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
            date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

            date_w_timezone = pytz.timezone("Europe/Helsinki").localize(parse_datetime(date_time), is_dst=None)

            tmp.arrive_time = date_w_timezone

            tmp.save()
            return redirect('/operator/bookings/')
    else:
        form = BookingPartenerForm(instance=BookingPartner.objects.get(id=pk))
    if request.user.is_superuser or Operator.objects.filter(user=request.user).exists():
        return render(request, 'operator/object_edit.html',
                      {"sections": ["Gestion", "Edition Réservation", str(pk)],
                       "form": form, "direct": 2, "title": "Réservations", "active": 4,
                       "sub_active": 1, "airports": Airport.objects.all(), "models": VehicleModel.objects.all(),
                       "custom": True, "clients": Client.objects.filter(partner__user=request.user),
                       "passengers_list": range(1, 7), "luggage_list": range(1, 6)})
    else:
        return redirect('/')
