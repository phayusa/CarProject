# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import pytz
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from AdminFront.forms import ClientFormNoUser, ClientForm
from AdminFront.forms import CommercialForm, BookingPartenerForm
from Back_Source.models import BuissnessPartner
from Back_Source.models import VehicleModel, Client, Airport
from Front.tokens import account_activation_token
from Front.views import compute_travel


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
        client_form = ClientFormNoUser(request.POST)
        partner = BuissnessPartner.objects.filter(user=request.user)[0]

        form_selector = request.POST.get('formselector', None)
        if not form_selector:
            return redirect('')

        # If the client already exist no need to create a new one
        if form_selector == "1":
            client = request.POST.get('client', None)
            if not client:
                raise Http404("Page non trouvé")
            if not request.POST._mutable:
                request.POST._mutable = True
            request.POST['client'] = client
            request.POST['status'] = "En cours de validation"
            request.POST['account'] = 0
            request.POST._mutable = False
        # Else we must create a new client
        elif form_selector == "2":

            if client_form.is_valid():
                client_obj = client_form.save(commit=False)
                # A temp user is created for the client
                username = client_obj.first_name + client_obj.last_name
                # We check if we don t have the same username
                if User.objects.filter(username=username):
                    suffix = 1
                    username_base = username
                    # We loop until we found a available username
                    while 1:
                        username = username_base + str(suffix)
                        if User.objects.filter(username=username):
                            suffix += 1
                        else:
                            break
                password = User.objects.make_random_password()
                user = User.objects.create_user(username=username, password=password, email=client_obj.mail)
                # Set the new user as inactive
                user.is_active = False
                user.save()

                # Send an email to the client to create the user
                current_site = get_current_site(request)
                subject = 'Aceline Services : Création de compte utilisateur'
                message = render_to_string('mail/mail_user_creation.html', {
                    'first_name': client_obj.first_name,
                    'username': username,
                    'password': password,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)

                # He must active it with an mail
                client_obj.user = user
                client_obj.partner = partner
                client_obj.save()
                client = client_obj.id
                if not request.POST._mutable:
                    request.POST._mutable = True
                    request.POST['status'] = "En cours de validation"
                    request.POST['account'] = 0
                    request.POST['client'] = client_obj
                    request.POST._mutable = False
            else:
                return redirect('/partener/booking/create/')

        form = BookingPartenerForm(request.POST)

        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.partner = partner

            date = request.POST.get('date', None)
            time = request.POST.get('time', None)

            raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
            date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

            date_w_timezone = pytz.timezone("Europe/Helsinki").localize(parse_datetime(date_time), is_dst=None)

            tmp.arrive_time = date_w_timezone
            tmp.client = Client.objects.filter(id=client)[0]

            origin = tmp.airport.address.replace(' ', '+').replace(',', '')
            destination = tmp.destination.replace(' ', '+').replace(',', '')

            estimation_travel = compute_travel(origin, destination, date_w_timezone)
            price = float(estimation_travel['distance']['text'].replace(" km", "")) * \
                    tmp.model_choose.price

            tmp.price = price
            tmp.time_estimated = int(estimation_travel['duration']['value'])

            tmp.save()
            return redirect('/partener/bookings/')
        print form.errors
    else:
        form = BookingPartenerForm()
        client_form = ClientFormNoUser(request.POST)

    if request.user.is_superuser or BuissnessPartner.objects.filter(user=request.user).exists():
        return render(request, 'partener/object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2, "active": 4,
                       "sub_active": 1, "title": "Création Réservation",
                       "airports": Airport.objects.all(), "models": VehicleModel.objects.all(),
                       "custom": True, "clients": Client.objects.filter(partner__user=request.user),
                       "passengers_list": range(1, 7), "luggage_list": range(1, 6), "creation": True,
                       "direct": 2, "user_form": client_form})
    else:
        return redirect('/')
