# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.timezone import datetime  # important if using timezones

from Back_Source.models import Area, Booking, BookingPartner, BookingCommecial, Driver
from Back_Source.models import Client
from common import test_admin_login


def index(request):
    if not test_admin_login(request.user):
        raise Http404("Page non trouvé")

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

    booking_current_year = Booking.objects.filter(date__year=datetime.today().year)
    booking_partener_current_year = BookingPartner.objects.filter(date__year=datetime.today().year)
    booking_commercial_current_year = BookingCommecial.objects.filter(date__year=datetime.today().year)

    booking_current_year_by_month = booking_current_year.annotate(month=ExtractMonth('date'))
    booking_partener_current_year_by_month = booking_partener_current_year.annotate(month=ExtractMonth('date'))
    booking_commercial_current_year_by_month = booking_commercial_current_year.annotate(month=ExtractMonth('date'))

    # Getting all the bookings by months
    booking_by_months = booking_current_year_by_month.values('month').annotate(count=Count('id')).values('month',
                                                                                                         'count')
    booking_partener_months = booking_partener_current_year_by_month.values('month').annotate(count=Count('id')).values(
        'month',
        'count')
    booking_commercial_months = booking_commercial_current_year_by_month.values('month').annotate(
        count=Count('id')).values(
        'month', 'count')

    gender_by_months = booking_current_year_by_month.values('month', 'client__gender').annotate(
        count=Count('id')).values(
        'month', 'count', 'client__gender')
    gender_partener_months = booking_partener_current_year_by_month.values('month', 'client__gender').annotate(
        count=Count('id')).values('month',
                                  'count', 'client__gender')
    gender_commercial_months = booking_commercial_current_year_by_month.values('month', 'client__gender').annotate(
        count=Count('id')).values(
        'month', 'count', 'client__gender')

    sum = booking_current_year.aggregate(Sum('price'))[u'price__sum']
    sum_commercial = booking_commercial_current_year.aggregate(
        Sum('price'))[u'price__sum']
    sum_partener = booking_commercial_current_year.aggregate(Sum(
        'price'))[u'price__sum']

    if not sum:
        sum = 0
    if not sum_commercial:
        sum_commercial = 0
    if not sum_partener:
        sum_partener = 0

    profit_on_year = sum_commercial + sum_partener + sum

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
                   "booking_by_months": all_bookings_by_months, "booking_gender": all_bookings_gender,
                   "profit": profit_on_year})
    # else:
    #     return redirect('/')


def base_manager(request):
    if not test_admin_login(request.user):
        raise Http404("Page non trouvé")

    if request.user.is_superuser:
        return render(request, 'admin_bis/person_manager.html', {"sections": ["Gestion Comptes"]})


def booking_manager(request):
    if not test_admin_login(request.user):
        raise Http404("Page non trouvé")

    if request.user.is_superuser:
        return render(request, 'admin_bis/booking_manager.html', {"sections": ["Gestion Réservation"]})


def car_manager(request):
    if not test_admin_login(request.user):
        raise Http404("Page non trouvé")

    return render(request, 'admin_bis/car_manager.html', {"sections": ["Gestion Voitures"]})


def areas(request):
    if not test_admin_login(request.user):
        raise Http404("Page non trouvé")

    if request.method == "GET":
        return render(request, 'admin_bis/areas.html',
                      {"sections": ["Carte", "Zones"], "areas": Area.objects.all(), "sub_active": 2})
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


def map_view(request):
    if not test_admin_login(request.user):
        raise Http404("Page non trouvé")

    return render(request, 'admin_bis/map.html', {"sections": ["Carte", "Temps Réels"], "sub_active": 1})

# def login_view(request):
#     if request.method == "GET":
#         return render(request, 'admin_bis/login.html')
#     else:
#         if request.method == "POST":
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 if user.is_superuser:
#                     return redirect('/admin/')
#                 return redirect('/')
#             else:
#                 return render(request, 'admin_bis/login.html')
