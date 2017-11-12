# -*- coding: utf-8 -*-


import datetime
import pytz

from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from geoposition import Geoposition

from Back_Source.models import VehicleModel, Client, Booking
from Localisation.views import upload_distance, set_booking_car
from forms import BookingForm
from django.utils.dateparse import parse_datetime


# Create your views here.


def index(request):
    return render(request, 'client/index-2.html')


def about(request):
    return render(request, 'client/about.html')


def not_found(request):
    return render(request, 'client/404.html')


def register(request):
    return render(request, 'client/login-register.html')


def prices(request):
    models = VehicleModel.objects.all()
    return render(request, 'client/prices.html', {'models': models})


def contact(request):
    return render(request, 'client/contact-us.html')


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


def booking_succeed(request):
    client = Client.objects.filter(user=request.user)[0]
    return render(request, 'client/success-payment.html', {"client": client})


def booking_create(request, *args, **kwargs):
    # print request.POST
    # return render(request, 'client/contact-us.html')
    data = request.POST
    form = BookingForm(data)
    # if form.is_valid():
    if not data['destination_0'] or not data['destination_1']:
        return redirect('/booking', {'form': form})
    if not data['departure_0'] or not data['departure_1']:
        return redirect('/booking', {'form': form})
    if not data['arrive_time']:
        return redirect('/booking', {'form': form})
    if not data['luggage_number']:
        return redirect('/booking', {'form': form})
    if not data['model_choose']:
        return redirect('/booking', {'form': form})
    if not data['passengers']:
        return redirect('/booking', {'form': form})
    date_w_timezone = pytz.timezone("Europe/Helsinki").localize(parse_datetime(data['arrive_time']), is_dst=None)
    booking = Booking.objects.create(destination=Geoposition(data['destination_0'], data['destination_1']),
                                     departure=Geoposition(data['departure_0'], data['departure_1']),
                                     arrive_time=date_w_timezone, luggage_number=int(data['luggage_number']),
                                     passengers=int(data['passengers']),
                                     model_choose=VehicleModel.objects.filter(id=data['model_choose'])[0],
                                     client=Client.objects.filter(id=data['client'])[0])
    upload_distance(booking)
    booking.save()
    after = timezone.now() + datetime.timedelta(hours=1)
    before = timezone.now() - datetime.timedelta(hours=1)
    #  If the booking is for the current moment update
    if before < booking.arrive_time < after:
        set_booking_car(booking)
    return render(request, 'client/payment.html')
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
        raw_date = datetime.datetime.strptime(date + ' ' + time, "%m/%d/%Y %I:%M %p")
        # tmp["arrive_time"] = raw_date.strftime("%d/%m/%Y %H:%M")
        tmp["arrive_time"] = raw_date.strftime("%Y-%m-%dT%H:%M")

    user_client = Client.objects.filter(user=request.user)
    if user_client:
        tmp["client"] = user_client[0]

    form = BookingForm(tmp)
    return render(request, 'client/booking.html', {'form': form})
