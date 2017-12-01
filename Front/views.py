# -*- coding: utf-8 -*-


import datetime

import pytz
from django.contrib.auth import login as login_func, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from Back_Source.models import VehicleModel, Client, Booking, Airport, BuissnessPartner, Commercial
from Localisation.views import upload_distance, set_booking_car
from forms import BookingForm, ClientForm


# Create your views here.


def index(request):
    # Redirect on the correct page
    if not request.user.is_authenticated():
        return render(request, 'client/index-2.html',
                      {"Airports": Airport.objects.all(), "cars": VehicleModel.objects.all()})

    if request.user.is_superuser:
        return redirect("/admin/")
    if BuissnessPartner.objects.filter(user=request.user).exists():
        return redirect("/partener/")
    if Commercial.objects.filter(user=request.user).exists():
        return redirect("/commercial/")

    return render(request, 'client/index-2.html',
                  {"Airports": Airport.objects.all(), "cars": VehicleModel.objects.all()})


def about(request):
    return render(request, 'client/about.html')


def not_found(request):
    return render(request, 'client/404.html')


def register(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # is_active=False)
            # user.save()
            # client = Client(user=user, mail=user.email, first_name=data['first_name'], last_name=data['last_name'],
            #                 age=int(data['age']), gender=data['gender'], phone_number=data['phone_number'])
            client = form.save()

            login_func(request, client.user)

            return redirect('/')
    else:
        form = ClientForm()

    return render(request, 'client/login-register.html', {"form": form})


def login(request):
    return render(request, 'client/login-register.html', {"type": 1})


def prices(request):
    models = VehicleModel.objects.all()
    return render(request, 'client/prices.html', {'models': models, "Airports": Airport.objects.all()})


def contact(request):
    return render(request, 'client/contact-us.html')


def contact_pro(request):
    if request.method == "POST":
        return redirect('/')
    return render(request, 'client/contact_pro.html')


def user(request):
    client = Client.objects.filter(user=request.user)[0]
    return render(request, 'client/user-profile.html', {"client": client})


def user_settings(request):
    client = Client.objects.filter(user=request.user)[0]
    return render(request, 'client/user-profile-settings.html', {"client": client})


def user_bookings(request):
    client = Client.objects.filter(user=request.user)[0]
    bookings = Booking.objects.filter(client=client)
    return render(request, 'client/user-profile-booking-history.html', {"client": client, "bookings": bookings})


def user_cards(request):
    client = Client.objects.filter(user=request.user)[0]
    bookings = Booking.objects.filter(client=client)
    return render(request, 'client/user-profile-cards.html', {"client": client, "bookings": bookings})


def user_bookings_delete(request, pk):
    # parsed_uri = urlparse(request.build_absolute_uri())
    # baseurl = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    # r = requests.delete(baseurl+'db/booking/'+pk, auth=(request.user.username, request.user.password))
    # print request.user.username
    # print request.user.password
    Booking.objects.filter(id=pk).delete()

    client = Client.objects.filter(user=request.user)[0]
    bookings = Booking.objects.filter(client=client)
    return render(request, 'client/user-profile-booking-history.html', {"client": client, "bookings": bookings})


def booking_succeed(request, pk):
    client = Client.objects.filter(user=request.user)[0]
    booking = Booking.objects.filter(id=pk)[0]
    return render(request, 'client/success-payment.html', {"client": client, "booking": booking})


def booking_create(request, *args, **kwargs):
    if not request.user.is_authenticated():
        return redirect('/login/')

    # print request.POST
    # return render(request, 'client/contact-us.html')
    data = request.POST
    # form = BookingForm(data)
    # # if form.is_valid():
    # if not data['destination_0'] or not data['destination_1']:
    #     return redirect('/booking', {'form': form})
    # if not data['departure_0'] or not data['departure_1']:
    #     return redirect('/booking', {'form': form})
    # if not data['arrive_time']:
    #     return redirect('/booking', {'form': form})
    # if not data['luggage_number']:
    #     return redirect('/booking', {'form': form})
    # if not data['model_choose']:
    #     return redirect('/booking', {'form': form})
    # if not data['passengers']:
    #     return redirect('/booking', {'form': form})
    date = data.get('date', None)
    time = data.get('time', None)

    clients = Client.objects.filter(user=request.user)
    if not clients:
        client = Client.objects.all()[0]
    else:
        client = clients[0]

    if not time or not date:
        return redirect('/')
    raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %I:%M %p")
    date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

    date_w_timezone = pytz.timezone("Europe/Helsinki").localize(parse_datetime(date_time), is_dst=None)
    booking, created = Booking.objects.get_or_create(destination=data["destination"],
                                                     destination_location=data["destination_location"].replace('(',
                                                                                                               '').replace(
                                                         ')',
                                                         ''),
                                                     airport=Airport.objects.filter(id=data["airport"])[0],
                                                     arrive_time=date_w_timezone,
                                                     luggage_number=int(data['luggage_number']),
                                                     passengers=int(data['passengers']),
                                                     model_choose=VehicleModel.objects.filter(id=data['model_choose'])[
                                                         0],
                                                     client=client,
                                                     flight=data["flight"])
    if not created:
        return redirect("/404/")
    upload_distance(booking)
    booking.save()
    after = timezone.now() + datetime.timedelta(hours=1)
    before = timezone.now() - datetime.timedelta(hours=1)
    #  If the booking is for the current moment update
    if before < booking.arrive_time < after:
        set_booking_car(booking)
    return render(request, 'client/payment.html', {"booking": booking})
    # else:
    #     return redirect('/booking', {'form': form})
    # parsed_uri = urlparse(request.build_absolute_uri())
    # baseurl = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    # post_data = {}
    # post_data['destination'] = Geoposition(data['destination_0'], data['destination_1'])
    # post_data['departure'] = Geoposition(data['departure_0'], data['departure_1'])
    # for key in data.keys():
    #     post_data[key] = data[key]
    #
    # print baseurl+'db/booking/create/'
    # result = urllib2.urlopen(baseurl+'db/booking/create/', urllib.urlencode(post_data))
    # content = result.read()
    # # print content
    # return render(request,content)


def booking(request, *args, **kwargs):
    # print request.GET.get('start','n,nbn')
    tmp = {}
    model = request.GET.get('model', None)
    if model:
        tmp["model_choose"] = model
    date = request.GET.get('date', None)
    time = request.GET.get('time', None)

    if time and date:
        raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %I:%M %p")
        # tmp["arrive_time"] = raw_date.strftime("%d/%m/%Y %H:%M")
        tmp["arrive_time"] = raw_date.strftime("%Y-%m-%dT%H:%M")

    user_client = Client.objects.filter(user=request.user)
    print user_client
    if user_client:
        tmp["client"] = user_client[0].id

    arrive = request.GET.get('arrive', None)
    airport = request.GET.get('airport', None)
    passengers = request.GET.get('passengers', None)

    if arrive:
        tmp["destination"] = arrive

    if airport:
        tmp["airport"] = airport

    if passengers:
        tmp["passengers"] = passengers

    form = BookingForm(tmp)
    return render(request, 'client/booking.html', {'form': form})
