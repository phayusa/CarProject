# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.shortcuts import render

from AdminFront.forms import ClientForm
from AdminFront.forms import DriverForm, CommercialForm, PartenerForm, BookingForm, AirportForm
from AdminFront.forms import BookingPartenerForm
from Back_Source.models import Client, Driver, BuissnessPartner, Commercial, Booking, Airport, BookingPartner


def client_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/partener/login')

    if request.method == "POST":
        form = ClientForm(request.POST, instance=Client.objects.get(id=pk))
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = BuissnessPartner.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/partener/manager/')
    else:
        form = ClientForm(instance=Client.objects.get(id=pk))
    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/object_edit.html',
                      {"sections": ["Gestion", "Edition Client", str(pk)],
                       "form": form, "title": "Clients", "active": 3,
                       "sub_active": 1})
    else:
        return redirect('/')


def commercial_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/partener/login')

    if request.method == "POST":
        form = CommercialForm(request.POST, instance=Commercial.objects.get(id=pk))
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = BuissnessPartner.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/partener/manager/')
    else:
        form = CommercialForm(instance=Commercial.objects.get(id=pk))
    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/object_edit.html',
                      {"sections": ["Gestion", "Edition Commerciaux", str(pk)],
                       "form": form, "title": "Commerciaux", "active": 3,
                       "sub_active": 1})
    else:
        return redirect('/')


def booking_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin_bis/login')

    if request.method == "POST":
        form = BookingPartenerForm(request.POST, instance=BookingPartner.objects.get(id=pk))
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = BuissnessPartner.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/admin_bis/bookings/')
    else:
        form = BookingPartenerForm(instance=BookingPartner.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'partener/object_edit.html',
                      {"sections": ["Gestion", "Edition Réservation", str(pk)],
                       "form": form, "direct": 2, "title": "Réservations", "active": 4,
                       "sub_active": 1})
    else:
        return redirect('/')
