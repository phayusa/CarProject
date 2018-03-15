# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.shortcuts import render

from AdminFront.forms import ClientForm, DriverForm, CommercialForm, PartenerForm, AirportForm
from AdminFront.forms import VehicleModelForm, VehicleForm


def client_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = ClientForm()
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2,
                       "title": "Client", "active": 3})
    else:
        return redirect('/')


def driver_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = DriverForm()
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2,
                       "title": "Chauffeur", "active": 3})
    else:
        return redirect('/')


def commercial_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = CommercialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = CommercialForm()
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2,
                       "title": "Commerciaux", "active": 3})
    else:
        return redirect('/')


def partener_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = PartenerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = PartenerForm()
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2,
                       "title": "Partenaires", "active": 3})
    else:
        return redirect('/')


def car_model_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = VehicleModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/cars/')
    else:
        form = VehicleModelForm()
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2, "direct": 3,
                       "title": "Modèle", "active": 5})
    else:
        return redirect('/')


def car_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            tmp = form.save(commit=False)

            tmp.empty_places = tmp.model.number_place
            tmp.empty_luggages = tmp.model.luggage_number

            tmp.save()
            return redirect('/admin/cars/')
        else:
            print form.errors
    else:
        form = VehicleForm()
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2, "direct": 3,
                       "title": "Voiture", "active": 5,
                       "file": True})
    else:
        return redirect('/')


def airport_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/bookings/')
    else:
        form = AirportForm()
    if request.user.is_superuser:
        return render(request, 'admin_bis/object_edit.html',
                      {"sections": ["Gestion", "Création Aéroport"],
                       "form": form, "direct": 2, "title": "Aéroports", "active": 4,
                       "sub_active": 1, "type": 2})
    else:
        return redirect('/')
