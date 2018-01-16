# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import groupby
from django.db.models import Count

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models.functions import ExtractMonth

from Back_Source.models import Area, Booking, BookingPartner, BookingCommecial, Driver
from Back_Source.models import Client
from django.utils.timezone import datetime  # important if using timezones


def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    # Getting the number of booking today
    today_booking = Booking.objects.filter(
        date__contains=datetime.today().date()).count() + BookingPartner.objects.filter(
        date__contains=datetime.today().date()).count() + BookingCommecial.objects.filter(
        date__contains=datetime.today().date()).count()

    # Getting the number of bookings by category
    booking_size = Booking.objects.filter(date__month=datetime.today().month).count()
    booking_partener_size = BookingPartner.objects.filter(date__month=datetime.today().month).count()
    booking_commercial_size = BookingCommecial.objects.filter(date__month=datetime.today().month).count()

    # Add it all to have the total for the month
    all_booking_month = booking_size + booking_partener_size + booking_commercial_size

    # Count the number of clients
    clients = Client.objects.count()

    # Count the number of drivers
    nb_driver = Driver.objects.all().count()

    booking_current_year = Booking.objects.filter(date__year=datetime.today().year).annotate(month=ExtractMonth('date'))
    booking_partener_current_year = BookingPartner.objects.filter(date__year=datetime.today().year).annotate(
        month=ExtractMonth('date'))
    booking_commercial_current_year = BookingCommecial.objects.filter(date__year=datetime.today().year).annotate(
        month=ExtractMonth('date'))

    # Getting all the bookings by months
    booking_by_months = booking_current_year.values('month').annotate(count=Count('id')).values('month', 'count')
    booking_partener_months = booking_partener_current_year.values('month').annotate(count=Count('id')).values('month',
                                                                                                               'count')
    booking_commercial_months = booking_commercial_current_year.values('month').annotate(count=Count('id')).values(
        'month', 'count')

    gender_by_months = booking_current_year.values('month', 'client__gender').annotate(count=Count('id')).values(
        'month', 'count', 'client__gender')
    gender_partener_months = booking_partener_current_year.values('month', 'client__gender').annotate(
        count=Count('id')).values('month',
                                  'count', 'client__gender')
    gender_commercial_months = booking_commercial_current_year.values('month', 'client__gender').annotate(
        count=Count('id')).values(
        'month', 'count', 'client__gender')

    # Add it in a new map
    all_bookings_by_months = {}
    all_bookings_gender = {}
    for month in xrange(1, 13):
        all_bookings_by_months[str(month)] = 0
        if booking_by_months.filter(month=month):
            all_bookings_by_months[str(month)] += booking_by_months.filter(month=month)[0]['count']

        if booking_partener_months.filter(month=month):
            all_bookings_by_months[str(month)] += booking_partener_months.filter(month=month)[0][
                'count']

        if booking_commercial_months.filter(month=month):
            all_bookings_by_months[str(month)] += booking_commercial_months.filter(month=month)[0][
                'count']

        all_bookings_gender[str(month)] = {}
        all_bookings_gender[str(month)]['Homme'] = 0
        all_bookings_gender[str(month)]['Femme'] = 0

        if gender_by_months.filter(month=month):
            for obj in gender_by_months.filter(month=month):
                if obj['client__gender'] == u'Homme':
                    all_bookings_gender[str(month)]['Homme'] += obj['count']
                if obj['client__gender'] == u'Femme':
                    all_bookings_gender[str(month)]['Femme'] += obj['count']

        if gender_partener_months.filter(month=month):
            for obj in gender_partener_months.filter(month=month):
                if obj['client__gender'] == u'Homme':
                    all_bookings_gender[str(month)]['Homme'] += obj['count']
                if obj['client__gender'] == u'Femme':
                    all_bookings_gender[str(month)]['Femme'] += obj['count']

        if gender_commercial_months.filter(month=month):
            for obj in gender_commercial_months.filter(month=month):
                if obj['client__gender'] == u'Homme':
                    all_bookings_gender[str(month)]['Homme'] += obj['count']
                if obj['client__gender'] == u'Femme':
                    all_bookings_gender[str(month)]['Femme'] += obj['count']

    # print all_bookings_gender
    # if request.user.is_superuser:
    return render(request, 'admin_bis/index3.html',
                  {"today_order": today_booking, "commercial_booking": booking_commercial_size,
                   "client_booking": booking_size, "partener_booking": booking_partener_size,
                   "clients": clients, "all": all_booking_month, "drivers": nb_driver,
                   "booking_by_months": all_bookings_by_months, "booking_gender": all_bookings_gender})
    # else:
    #     return redirect('/')


# def get_month_label(month):
#     if month == 1:
#         return 'jan'
#     elif month == 2:
#         return 'fev'
#     elif month == 3:
#         return 'mars'
#     elif month == 4:
#         return 'avril'
#     elif month == 5:
#         return 'mai'
#     elif month == 6:
#         return 'juin'
#     elif month == 7:
#         return 'juillet'
#     elif month == 8:
#         return 'août'
#     elif month == 9:
#         return 'sept'
#     elif month == 10:
#         return 'oct'
#     elif month == 11:
#         return 'nov'
#     elif month == 12:
#         return 'dec'


def base_manager(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        return render(request, 'admin_bis/person_manager.html', {"sections": ["Gestion Comptes"]})
    else:
        return redirect('/')


def booking_manager(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        return render(request, 'admin_bis/booking_manager.html', {"sections": ["Gestion Réservation"]})
    else:
        return redirect('/')


def car_manager(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        return render(request, 'admin_bis/car_manager.html', {"sections": ["Gestion Voitures"]})
    else:
        return redirect('/')


def areas(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        if request.method == "GET":
            return render(request, 'admin_bis/areas.html', {"sections": ["Zones"], "areas": Area.objects.all()})
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
        return render(request, 'admin_bis/login.html')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin/')
                return redirect('/')
            else:
                return render(request, 'admin_bis/login.html')
