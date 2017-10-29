import datetime
import json
import urllib2

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from Back_Source.models import Booking
from Back_Source.models import Vehicle, Area
from Back_Source.models import Driver, Travel

from django.conf import settings


# Create your views here.
def mapView(request):
    pois = Vehicle.objects.all()
    return render(request, 'test_map.html', {'pois': pois})


def mapView2(request):
    pois = Vehicle.objects.all()
    return render(request, 'test_map2.html', {'pois': pois})


def get_area(booking):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + \
          booking.destination.replace(" ",
                                      "+") + '&key=' + getattr(settings, "GEOPOSITION_GOOGLE_MAPS_API_KEY", None)
    serialized_data = urllib2.urlopen(url).read()

    data = json.loads(serialized_data)["results"][0]["geometry"]["location"]
    # print data
    for area in Area.objects.all():
        if (area.south < data['lat'] < area.north) and (area.west < data['lng'] < area.east):
            return area


def set_booking_driver(booking):
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
    # area_vehicle.
    area_vehicle.save()

    booking.vehicle_choose = area_vehicle
    # booking.travel.car = area_vehicle
    # booking.travel.driver = area_vehicle.driver
    booking.save()

    travel, _ = Travel.objects.get_or_create(car=area_vehicle)
    travel.bookings.add(booking)
    travel.save()


def upload_bookings_vehicle(request):
    # if not request.user.is_superuser:
    #     return HttpResponse('The user is not superuser')
    bookings_to_assigned = Booking.objects.filter(arrive_time__lte=(timezone.now() + datetime.timedelta(hours=1)),
                                                  arrive_time__gte=timezone.now(), vehicle_choose=None)
    for booking in bookings_to_assigned:
        set_booking_driver(booking)

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
