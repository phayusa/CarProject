# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.timezone import datetime  # important if using timezones

from Back_Source.models import BookingPartner, BookingCommecial
from Back_Source.models.person import Client, BuissnessPartner


def index(request):
    if not request.user.is_authenticated():
        return redirect('/partener/login')

    today_booking = BookingPartner.objects.filter(
        date__contains=datetime.today().date(), partner__user=request.user).count() + BookingCommecial.objects.filter(
        date__contains=datetime.today().date(), commercial__partner__user=request.user).count()

    # Getting the number of bookings by category
    booking_partener_size = BookingPartner.objects.filter(date__month=datetime.today().month,
                                                          partner__user=request.user).count()
    booking_commercial_size = BookingCommecial.objects.filter(date__month=datetime.today().month,
                                                              commercial__partner__user=request.user).count()

    # All booking from start
    booking_all = BookingPartner.objects.filter(partner__user=request.user).count() + BookingCommecial.objects.filter(
        commercial__partner__user=request.user).count()

    # Add it all to have the total for the month
    all_booking_month = booking_partener_size + booking_commercial_size

    # Count the number of clients
    clients = Client.objects.filter(partner__user=request.user).count()

    booking_partener_current_year = BookingPartner.objects.filter(date__year=datetime.today().year,
                                                                  partner__user=request.user)

    booking_partener_current_year_by_month = booking_partener_current_year.annotate(month=ExtractMonth('date'))

    booking_commercial_current_year = BookingCommecial.objects.filter(date__year=datetime.today().year,
                                                                      commercial__partner__user=request.user)

    booking_commercial_current_year_by_month = booking_commercial_current_year.annotate(month=ExtractMonth('date'))

    # Getting all the bookings by months
    booking_partener_months = booking_partener_current_year_by_month.values('month').annotate(count=Count('id')).values(
        'month',
        'count')
    booking_commercial_months = booking_commercial_current_year_by_month.values('month').annotate(
        count=Count('id')).values(
        'month', 'count')

    gender_partener_months = booking_partener_current_year_by_month.values('month', 'client__gender').annotate(
        count=Count('id')).values('month',
                                  'count', 'client__gender')
    gender_commercial_months = booking_commercial_current_year_by_month.values('month', 'client__gender').annotate(
        count=Count('id')).values(
        'month', 'count', 'client__gender')

    sum_commercial = booking_commercial_current_year.aggregate(
        Sum('price'))[u'price__sum']
    sum_partener = booking_commercial_current_year.aggregate(Sum(
        'price'))[u'price__sum']

    if not sum_commercial:
        sum_commercial = 0
    if not sum_partener:
        sum_partener = 0

    profit_on_year = sum_commercial + sum_partener

    # Add it in a new map
    all_bookings_by_months = {}
    all_bookings_gender = {}
    for month in xrange(1, 13):
        all_bookings_by_months[str(month)] = 0
        if booking_partener_months.filter(month=month):
            all_bookings_by_months[str(month)] += booking_partener_months.filter(month=month)[0][
                'count']

        if booking_commercial_months.filter(month=month):
            all_bookings_by_months[str(month)] += booking_commercial_months.filter(month=month)[0][
                'count']

        all_bookings_gender[str(month)] = {}
        all_bookings_gender[str(month)]['Homme'] = 0
        all_bookings_gender[str(month)]['Femme'] = 0

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

    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/index.html',
                      {"today_order": today_booking, "commercial_booking": booking_commercial_size,
                       "partener_booking": booking_partener_size,
                       "clients": clients, "all": all_booking_month,
                       "booking_by_months": all_bookings_by_months, "booking_gender": all_bookings_gender,
                       "bookings_start": booking_all, "profit": profit_on_year})
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

