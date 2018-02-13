import datetime

import pytz
import stripe
from django.contrib.auth import login as login_func, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import *
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from Back_Source.models import VehicleModel, Client, Booking, Airport, BuissnessPartner, Commercial, Operator
from forms import BookingForm, BookingCreateFormClient, ClientForm, ClientFormNoUser, ContactUsForm, ContactProForm
from tokens import account_activation_token

# Library for generate PDF
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import json
import urllib

# Create your views here.


def index(request):
    # Redirect on the correct page

    if not request.user.is_authenticated():
        return render(request, 'client/index-2.html')

    if request.user.is_superuser:
        return redirect("/admin/")

    # if BuissnessPartner.objects.filter(user=request.user).exists:
    #     return redirect("/partener/")

    if Commercial.objects.filter(user=request.user).exists():
        return redirect("/commercial/")

    if request.method == 'GET':
        return render(request, 'client/index-2.html')
    else:
        return redirect("/404")


def login(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if not username:
            errors['username'] = 'Champs requis'
        if not password:
            errors['password'] = 'Champs requis'
            return render(request, 'client/login-register.html', {"type": 1, "errors": errors})

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login_func(request, user)
                # Force the user logout after 5 minutes of inactivity
                request.session.set_expiry(3000)
                return HttpResponseRedirect('/')
        else:
            errors['username'] = 'Nom d\'utilisateur ou Mot de passe incorrecte'
    return render(request, 'client/login-register.html', {"type": 1, "errors": errors})


def register(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        client = form.save()
        user_client = client.user
        current_site = get_current_site(request)

        subject = 'Aceline Services : confirmation du compte'
        message =  render_to_string('mail/mail_confirmation.html', {
            'user': user_client,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user_client.pk)),
            'token': account_activation_token.make_token(user_client)
        })
        user_client.email_user(subject, message)
        return redirect('account_activation_sent')
    else:
        form = ClientForm()

    return render(request, 'client/login-register.html', {"form": form})


def user(request):
    client = Client.objects.filter(user=request.user)[0]
    return render(request, 'client/user-profile.html', {"client": client})


def user_settings(request):
    client = Client.objects.filter(user=request.user)[0]
    return render(request, 'client/user-profile-settings.html', {"client": client})


def not_found(request):
    return render(request, 'client/404.html')


def about(request):
    return render(request, 'client/about.html')


def how_it_works(request):
    return render(request, 'client/howItWorks.html')


def booking(request, *args, **kwargs):

    if request.method == 'GET':
        form = BookingCreateFormClient()
        client_form = ClientFormNoUser()
        return render(request, 'client/bookingInterface.html',
                      {"Airports": Airport.objects.all(),
                       "cars": VehicleModel.objects.all(),
                       "form": form,
                       "clientForm": client_form})

    if request.method == 'POST':
        form = BookingCreateFormClient(request.POST)
        client_form = ClientFormNoUser(request.POST)
        data = request.POST
        date = data.get('date', None)
        time = data.get('time', None)
        print "the date is %s", date

        if request.user.is_authenticated:
            clients = Client.objects.filter(user=request.user)
            print "user : ", request.user
            print "Client connected : ", clients

            if not clients:
                client = Client.objects.all()[0]
            else:
                client = clients[0]

        else:
            if client_form.is_valid():
                # print "Client_form is valid"
                # print client_form

                client_obj = client_form.save(commit=False)

                first_name = (client_form.cleaned_data['first_name']).replace(' ', '').replace('-', '')
                last_name = (client_form.cleaned_data['last_name']).replace(' ', '').replace('-', '')
                mail = client_form.cleaned_data['mail']

                # The login of the user is the first letter of the last_name and his first_name
                client_identification = last_name[0] + first_name

                if User.objects.filter(username=client_identification):
                    suffix = 1
                    username_base = client_identification
                    # We loop until we found a available username
                    while 1:
                        username = username_base + str(suffix)
                        if User.objects.filter(username=username):
                            suffix += 1
                        else:
                            client_identification = username
                            break

                password = User.objects.make_random_password()
                print "the identifiant is : ", client_identification
                print "the password is : ", password
                login_user = User.objects.create_user(client_identification, mail, password)
                login_user.save()

                client_obj.user = login_user
                client_obj.save()
                client_id = client_obj.id
                client = Client.objects.filter(id=client_id)[0]

        if form.is_valid():
            # print "BookingCreateFormClient is valid"
            # print form

            raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")#(date, "%Y-%m-%d")  #

            date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

            date_w_timezone = pytz.timezone("Europe/Paris").localize(parse_datetime(date_time), is_dst=None)

            booking_no_user = Booking.objects.create(destination=data["destination"],
                                                     destination_location=data["destination_location"].replace('(', '')
                                                                                                      .replace(')', ''),
                                                     airport=Airport.objects.filter(id=data["airport"])[0],
                                                     # time_booking= datetimeNow.strftime("%d/%m/%Y %H:%M"),
                                                     arrive_time=date_w_timezone,
                                                     luggage_number=int(data['luggage_number']),
                                                     client=client,
                                                     passengers=int(data['passengers']))

        request.session['Booking_id'] = booking_no_user.id
        request.session.modified = True
        return redirect('/booking/payment')


def booking_payment(request):
    booking_pending_id = request.session.get("Booking_id", False)
    if not booking_pending_id:
        raise Http404("Page not found")
    if request.method == 'GET':
        print "In the get !"
        booking_pending = Booking.objects.filter(id=booking_pending_id).first()
        return render(request, 'client/payment.html', {"booking": booking_pending})
    elif request.method == 'POST':
        booking_pending = Booking.objects.filter(id=booking_pending_id).first()
        print "In the post !"

    # TODO : stripe
