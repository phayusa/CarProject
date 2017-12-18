# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import pytz
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.dateparse import parse_datetime

from AdminFront.forms import ClientForm, CommercialForm, BookingOperatorForm
from Back_Source.models import VehicleModel, Client, Airport, Operator


def client_create(request):
    if not request.user.is_authenticated():
        return redirect('/operator/login')

    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = Operator.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/operator/manager/')
    else:
        form = ClientForm()

    if request.user.is_superuser or Operator.objects.filter(user=request.user).exists():

        return render(request, 'operator/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2})
    else:
        return redirect('/')


def commercial_create(request):
    if not request.user.is_authenticated():
        return redirect('/operator/login')

    if request.method == "POST":
        form = CommercialForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = Operator.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/operator/manager/')
    else:
        form = CommercialForm()
    if request.user.is_superuser or Operator.objects.filter(user=request.user).exists():
        return render(request, 'operator/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2})
    else:
        return redirect('/')


def booking_create(request):
    if not request.user.is_authenticated():
        return redirect('/operator/login')

    if request.method == "POST":
        form_client = ClientForm()
        form = BookingOperatorForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.operator = Operator.objects.filter(user=request.user)[0]

            date = request.POST.get('date', None)
            time = request.POST.get('time', None)

            raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
            date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

            date_w_timezone = pytz.timezone("Europe/Helsinki").localize(parse_datetime(date_time), is_dst=None)

            tmp.arrive_time = date_w_timezone
            tmp.save()
            return redirect('/operator/bookings/')
        print form.errors
    else:
        form = BookingOperatorForm()
        form_client = ClientForm()

    if request.user.is_superuser or Operator.objects.filter(user=request.user).exists():
        return render(request, 'operator/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2, "active": 4,
                       "sub_active": 1, "title": "Création Réservation",
                       "airports": Airport.objects.all(), "models": VehicleModel.objects.all(),
                       "custom": True, "clients": Client.objects.filter(partner__user=request.user),
                       "passengers_list": range(1, 7), "luggage_list": range(1, 6), "creation": True,
                       "direct": 2})
    else:
        return redirect('/')
