# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.shortcuts import render

from Back_Source.models import Client, Driver, BuissnessPartner, Commercial, Booking, Airport
from AdminFront.forms import ClientForm, DriverForm, CommercialForm, PartenerForm, UserForm, BookingForm, AirportForm


def client_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = ClientForm(request.POST, instance=Client.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = ClientForm(instance=Client.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Edition Client", str(pk)],
                       "form": form, "title": "Clients", "active": 3,
                       "sub_active": 1})
    else:
        return redirect('/')


def driver_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = DriverForm(request.POST, instance=Driver.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = DriverForm(instance=Driver.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Edition Chauffeurs", str(pk)],
                       "form": form, "title": "Chauffeurs", "active": 3,
                       "sub_active": 1})
    else:
        return redirect('/')


def commercial_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = CommercialForm(request.POST, instance=Commercial.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = CommercialForm(instance=Commercial.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Edition Commerciaux", str(pk)],
                       "form": form, "title": "Commerciaux", "active": 3,
                       "sub_active": 1})
    else:
        return redirect('/')


def partener_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = PartenerForm(request.POST, instance=BuissnessPartner.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = PartenerForm(instance=BuissnessPartner.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Edition Partenaire Commercial", str(pk)],
                       "form": form, "title": "Partenaire Commerciaux", "active": 3,
                       "sub_active": 1})
    else:
        return redirect('/')


def booking_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = BookingForm(request.POST, instance=Booking.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/bookings/')
    else:
        form = BookingForm(instance=Booking.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Edition Réservation", str(pk)],
                       "form": form, "direct": 2, "title": "Réservations", "active": 4,
                       "sub_active": 1})
    else:
        return redirect('/')


def airport_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = AirportForm(request.POST, instance=Airport.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/bookings/')
    else:
        form = AirportForm(instance=Airport.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Edition Aéroport", str(pk)],
                       "form": form, "direct": 2, "title": "Aéroports", "active": 4,
                       "sub_active": 1})
    else:
        return redirect('/')
