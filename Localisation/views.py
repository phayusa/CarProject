import datetime
import json
import math
import urllib2

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from Back_Source.models import Booking
from Back_Source.models import Driver, Travel
from Back_Source.models import Vehicle, Area


# Create your views here.
def mapView(request):
    pois = Vehicle.objects.all()
    return render(request, 'test_map.html', {'pois': pois})


def mapView2(request):
    pois = Vehicle.objects.all()
    return render(request, 'test_map2.html', {'pois': pois})


def autocomplete(request):
    return render(request, 'autocomplete.html')


def get_area(booking):
    data = LocationObj(booking.destination_location)
    for area in Area.objects.all():
        if (area.south < data.latitude < area.north) and (area.west < data.longitude < area.east):
            return area


def set_booking_car(booking):
    area = get_area(booking)
    area_vehicles = Vehicle.objects.filter(travelling=False, empty_places__gte=booking.passengers,
                                           empty_luggages__gte=booking.luggage_number, area=area)
    # print "1 "+str(area_vehicles)
    if not area_vehicles:
        area_vehicles = Vehicle.objects.filter(travelling=False, empty_places__gte=booking.passengers,
                                               empty_luggages__gte=booking.luggage_number, area=None)
        if not area_vehicles:
            return
            # return HttpResponse('Error no vehicle available')
    area_vehicle = area_vehicles[0]
    area_vehicle.area = area
    area_vehicle.empty_places -= booking.passengers
    area_vehicle.empty_luggages -= booking.luggage_number
    # area_vehicle.
    area_vehicle.save()

    booking.vehicle_choose = area_vehicle
    # booking.travel.car = area_vehicle
    # booking.travel.driver = area_vehicle.driver
    booking.save()

    travel, _ = Travel.objects.get_or_create(car=area_vehicle)
    travel.bookings.add(booking)
    if area_vehicle.driver:
        travel.driver = area_vehicle.driver
    travel.save()


def give_order_booking(request):
    if not request.user:
        return
    drivers = Driver.objects.filter(user=request.user)
    if not drivers:
        return
    driver = drivers[0]
    vehicles = Vehicle.objects.filter(driver=driver)
    if not vehicles:
        return
    vehicle = vehicles[0]
    travels = Travel.objects.filter(car=vehicle, driver=driver, start=None)
    if not travels:
        return
    travel = travels[0]
    return travel.bookings.order_by('distance')


def upload_bookings_vehicle(request):
    # if not request.user.is_superuser:
    #     return HttpResponse('The user is not superuser')
    bookings_to_assigned = Booking.objects.filter(arrive_time__lte=(timezone.now() + datetime.timedelta(hours=1)),
                                                  arrive_time__gte=timezone.now(), vehicle_choose=None)
    for booking in bookings_to_assigned:
        set_booking_car(booking)

    return HttpResponse("OK")


def end_driver(request):
    driver = Driver.objects.filter(user=request.user)
    if not driver:
        return HttpResponse("Unauthorized")

    vehicle = Vehicle.objects.filter(driver=driver)[0]
    if not vehicle:
        return HttpResponse("Bad Request")
    vehicle.area = None
    vehicle.driver = None
    vehicle.save()


class LocationObj():
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0

    def __init__(self, str_pos):
        tmp = str_pos.replace("(", "").replace(")", "").split(",")
        self.latitude = float(tmp[0])
        self.longitude = float(tmp[1])


def upload_distance(booking):
    points_destination = LocationObj(booking.destination_location)
    points_depart = LocationObj(booking.airport.location)
    booking.distance = math.hypot(points_destination.latitude - points_depart.latitude,
                                  points_destination.longitude - points_depart.longitude)
    booking.save()
