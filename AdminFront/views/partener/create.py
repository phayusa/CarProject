# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.shortcuts import render

from AdminFront.forms import ClientForm, CommercialForm, BookingPartenerForm
from Back_Source.models import BuissnessPartner, Airport, VehicleModel


def client_create(request):
    if not request.user.is_authenticated():
        return redirect('/partener/login')

    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = BuissnessPartner.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/partener/manager/')
    else:
        form = ClientForm()

    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():

        return render(request, 'partener/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2})
    else:
        return redirect('/')


def commercial_create(request):
    if not request.user.is_authenticated():
        return redirect('/partener/login')

    if request.method == "POST":
        form = CommercialForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = BuissnessPartner.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/partener/manager/')
    else:
        form = CommercialForm()
    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2})
    else:
        return redirect('/')


def booking_create(request):
    if not request.user.is_authenticated():
        return redirect('/partener/login')

    if request.method == "POST":
        print request.POST
        form = BookingPartenerForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)

            print tmp

            tmp.partner = BuissnessPartner.objects.filter(user=request.user)[0]
            tmp.save()
            return redirect('/partener/manager/')
        print form.errors
    else:
        form = BookingPartenerForm()
    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2, "active": 4,
                       "sub_active": 1, "title": "Création Réservation",
                       "airports": Airport.objects.all(), "models": VehicleModel.objects.all(),
                       "custom": True})
    else:
        return redirect('/')
