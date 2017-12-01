# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import pytz
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
# from django.utils.timezone import datetime  # important if using timezones

from AdminFront.forms import BookingCommercialEditForm, BookingCommercialCreateForm, ClientFormNoUser, ClientForm
from Back_Source.models.person import Client, Commercial, BuissnessPartner
from Back_Source.models.location import Airport
from Back_Source.models.vehicle import VehicleModel
from Back_Source.models.booking import BookingCommecial

from django.contrib.auth.forms import UserCreationForm


def index(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    if not Commercial.objects.filter(user=request.user).exists():
        return redirect('/')

    commercial = Commercial.objects.filter(user=request.user)[0]
    client = request.POST.get('client', None)
    if not client:
        redirect('/')

    if request.method == "POST":

        form = BookingCommercialCreateForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.commercial = commercial

            date = request.POST.get('date', None)
            time = request.POST.get('time', None)

            raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
            date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

            date_w_timezone = pytz.timezone("Europe/Helsinki").localize(parse_datetime(date_time), is_dst=None)

            tmp.arrive_time = date_w_timezone

            tmp.client = Client.objects.filter(id=client)[0]

            tmp.save()
            return redirect('/commercial/')
    else:
        form = BookingCommercialCreateForm()

    if request.user.is_superuser or Commercial.objects.filter(user=request.user).exists():
        commercial = Commercial.objects.filter(user=request.user)[0]
        if not commercial.partner:
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(partner=commercial.partner)
        return render(request, 'commercial/booking.html',
                      {"sections": ["Réserver"],
                       "form": form, "type": 2, "active": 1,
                       "title": "Réservation",
                       "airports": Airport.objects.all(), "models": VehicleModel.objects.all(),
                       "custom": True, "clients": clients,
                       "passengers_list": range(1, 7), "luggage_list": range(1, 6), "creation": True,
                       "direct": 2})
    else:
        return redirect('/')


def edit_booking(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login/')
    if not Commercial.objects.filter(user=request.user).exists():
        return redirect('/')

    commercial = Commercial.objects.filter(user=request.user)[0]
    booking = BookingCommecial.objects.filter(id=pk)[0]

    if not commercial or not booking:
        return redirect('/404/')

    if request.method == "POST":

        client = request.POST.get('client', None)
        if not client:
            return redirect('/404/')

        form = BookingCommercialEditForm(request.POST, instance=booking)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.commercial = commercial

            date = request.POST.get('date', None)
            time = request.POST.get('time', None)

            raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
            date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

            date_w_timezone = pytz.timezone("Europe/Helsinki").localize(parse_datetime(date_time), is_dst=None)

            tmp.arrive_time = date_w_timezone

            tmp.client = Client.objects.filter(id=client)[0]

            tmp.save()
            return redirect('/commercial/')
    else:
        form = BookingCommercialEditForm(instance=booking)

    if request.user.is_superuser or Commercial.objects.filter(user=request.user).exists():
        commercial = Commercial.objects.filter(user=request.user)[0]
        if not commercial.partner:
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(partner=commercial.partner)
        return render(request, 'commercial/object_edit.html',
                      {"sections": ["Réserver", "Modification Réservation", str(pk)],
                       "form": form, "active": 1,
                       "title": "Modfication Réservation",
                       "airports": Airport.objects.all(), "models": VehicleModel.objects.all(),
                       "custom": True, "clients": clients,
                       "passengers_list": range(1, 7), "luggage_list": range(1, 6), "creation": True,
                       "direct": 2})
    else:
        return redirect('/')


def clients_list(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    if not Commercial.objects.filter(user=request.user).exists():
        return redirect('/')

    commercial = Commercial.objects.filter(user=request.user)[0]

    if request.method == "POST":

        form = ClientFormNoUser(request.POST)
        user_form = UserCreationForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            user = user_form.save()

            tmp = form.save(commit=False)
            tmp.partner = commercial.partner
            tmp.user = user

            tmp.save()
            return redirect('/commercial/clients/')
    else:
        form = ClientFormNoUser()
        user_form = UserCreationForm()

    if request.user.is_superuser or Commercial.objects.filter(user=request.user).exists():
        commercial = Commercial.objects.filter(user=request.user)[0]
        if not commercial.partner:
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(partner=commercial.partner)
        return render(request, 'commercial/user.html',
                      {"sections": ["Clients"],
                       "form": form, "type": 2, "active": 2,
                       "title": "Clients", "user_form": user_form,
                       "custom": True, "clients": clients,
                       "creation": True, "direct": 2})
    else:
        return redirect('/')


def clients_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/login/')
    if not Commercial.objects.filter(user=request.user).exists():
        return redirect('/')

    try:
        commercial = Commercial.objects.filter(user=request.user)[0]
        client = Client.objects.filter(id=pk)[0]
    except Exception:
        return redirect('/')

    if request.method == "POST":

        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = commercial.partner

            tmp.save()
            return redirect('/commercial/clients/')
    else:
        form = ClientForm(instance=client)

    if request.user.is_superuser or Commercial.objects.filter(user=request.user).exists():
        commercial = Commercial.objects.filter(user=request.user)[0]
        if not commercial.partner:
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(partner=commercial.partner)
        return render(request, 'commercial/user.html',
                      {"sections": ["Clients"],
                       "form": form, "type": 1, "active": 2,
                       "title": "Clients", "clients": clients,
                       "direct": 2})
    else:
        return redirect('/')
