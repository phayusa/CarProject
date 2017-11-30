# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render

from Back_Source.models import Area, Booking, BookingPartner, BookingCommecial
from Back_Source.models.person import Client, BuissnessPartner
from django.utils.timezone import datetime  # important if using timezones


def index(request):
    if not request.user.is_authenticated():
        return redirect('/partener/login')

    today_booking = BookingPartner.objects.filter(
        date__contains=datetime.today().date(), partner__user=request.user).count() + BookingCommecial.objects.filter(
        date__contains=datetime.today().date(), commercial__partner__user=request.user).count()

    booking_partener_size = BookingPartner.objects.filter(date__month=datetime.today().month,
                                                          partner__user=request.user).count()
    booking_commercial_size = BookingCommecial.objects.filter(date__month=datetime.today().month,
                                                              commercial__partner__user=request.user).count()

    clients = Client.objects.count()

    all_booking_month = booking_partener_size + booking_commercial_size

    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/index.html',
                      {"today_order": today_booking, "commercial_booking": booking_commercial_size,
                       "partener_booking": booking_partener_size,
                       "clients": clients, "all": all_booking_month})
    else:
        return redirect('/404/')


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
