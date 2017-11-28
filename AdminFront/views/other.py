# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render

from Back_Source.models import Area, Booking, BookingPartner, BookingCommecial
from Back_Source.models import Client
from django.utils.timezone import datetime  # important if using timezones


def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    today_booking = Booking.objects.filter(
        date__contains=datetime.today().date()).count() + BookingPartner.objects.filter(
        date__contains=datetime.today().date()).count() + BookingCommecial.objects.filter(
        date__contains=datetime.today().date()).count()

    booking_size = Booking.objects.filter(date__month=datetime.today().month).count()
    booking_partener_size = BookingPartner.objects.filter(date__month=datetime.today().month).count()
    booking_commercial_size = BookingCommecial.objects.filter(date__month=datetime.today().month).count()

    clients = Client.objects.count()

    if request.user.is_superuser:
        return render(request, 'ui-elements-charts.html',
                      {"today_order": today_booking, "commercial_booking": booking_commercial_size,
                       "client_booking": booking_size, "partener_booking": booking_partener_size,
                       "clients": clients})
    else:
        return redirect('/')


def base_manager(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        return render(request, 'person_manager.html', {"sections": ["Gestion Comptes"]})
    else:
        return redirect('/')


def booking_manager(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        return render(request, 'booking_manager.html', {"sections": ["Gestion Réservation"]})
    else:
        return redirect('/')


def areas(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        if request.method == "GET":
            return render(request, 'areas.html', {"sections": ["Zones"], "areas": Area.objects.all()})
        else:
            if request.method == "POST":
                data = request.POST
                print data
                for area in Area.objects.all():
                    print area.id
                    if str(area.id) in data:
                        raw_data = data[str(area.id)].replace(",", ".").split(";")
                        if len(raw_data) == 4:
                            area.north = raw_data[0]
                            area.south = raw_data[1]
                            area.west = raw_data[2]
                            area.east = raw_data[3]
                            area.save()
                return redirect("/admin/areas/")
    else:
        return redirect('/')


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin')
                return redirect('/')
            else:
                return render(request, 'login.html')
