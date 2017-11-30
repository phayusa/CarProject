# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import pytz
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.utils.timezone import datetime  # important if using timezones

from AdminFront.forms import BookingCommercialForm
from Back_Source.models.person import Client, Commercial, BuissnessPartner
from Back_Source.models.location import Airport
from Back_Source.models.vehicle import VehicleModel

from django.contrib.auth.forms import UserCreationForm


def index(request):
    if not request.user.is_authenticated():
        return redirect('/partener/login')
    if not Commercial.objects.filter(user=request.user).exists():
        return redirect('/404/')

    commercial = Commercial.objects.filter(user=request.user)[0]

    if request.method == "POST":
        type = request.POST.get("formselector", None)
        if not type:
            redirect("/")
        print type

        form = BookingCommercialForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.commercial = commercial

            date = request.POST.get('date', None)
            time = request.POST.get('time', None)

            raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
            date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

            date_w_timezone = pytz.timezone("Europe/Helsinki").localize(parse_datetime(date_time), is_dst=None)

            tmp.arrive_time = date_w_timezone
            tmp.save()
            return redirect('/partener/bookings/')
        print form.errors
    else:
        form = BookingCommercialForm()

    if request.user.is_superuser or Commercial.objects.filter(user=request.user).exists():
        commercial = Commercial.objects.filter(user=request.user)[0]
        if not commercial.partner:
            clients = Client.objects.all()
        else:
            clients = Client.objects.filter(partner=commercial.partner)
        return render(request, 'commercial/reservation.html',
                      {"sections": ["Réserver"],
                       "form": form, "type": 2, "active": 1,
                       "title": "Création Réservation",
                       "airports": Airport.objects.all(), "models": VehicleModel.objects.all(),
                       "custom": True, "clients": clients,
                       "passengers_list": range(1, 7), "luggage_list": range(1, 6), "creation": True,
                       "direct": 2, "user_form": UserCreationForm()})
    else:
        return redirect('/')


def base_manager(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/person_manager.html', {"sections": ["Gestion Comptes"]})
    else:
        return redirect('/')


def booking_manager(request):
    if not request.user.is_authenticated():
        return redirect('/partener/login')

    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/booking_manager.html', {"sections": ["Gestion Réservation"]})
    else:
        return redirect('/')


def login_view(request):
    if request.method == "GET":
        return render(request, 'admin_bis/login.html')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser or BuissnessPartner.objects.filter(user=user).exists():
                    return redirect('/partener/')
                return redirect('/')
            else:
                return render(request, 'admin/login.html')
