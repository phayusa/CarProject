from django.http import HttpResponse

from django.shortcuts import render
from Back_Source.models import Vehicle, Area
from django.shortcuts import render
from Back_Source.models import Travel, Booking
from Localisation.models.primitives import Rectangle, Point
from rest_framework.views import APIView
import datetime
from django.utils import timezone


# Point 1 48.868319 2.146119 (haut gauche)
# Point 2 48.863350 2.344559 (haut droite)
# Point 3 48.765232 2.126893 (bas gauche)
# Point 4 48.746219 2.345933 (bas droite)


# Create your views here.
def mapView(request):
    pois = Vehicle.objects.all()
    return render(request, 'test_map.html', {'pois': pois})


def mapView2(request):
    pois = Vehicle.objects.all()
    return render(request, 'test_map2.html', {'pois': pois})


def set_booking_driver(booking):
    for area in Area.objects.all():
        object_area = Rectangle(Point(area.east, area.south), area.west - area.east, area.north - area.south)
        # if (object_area.contains())


def set_driver(request):
    if not request.user.is_superuser:
        return HttpResponse('The user is not superuser')
    bookings_to_assigned = Booking.objects.filter(arrive_time__lte=(timezone.now() + datetime.timedelta(hours=1)),
                                                  arrive_time__gte=timezone.now())
    for booking in bookings_to_assigned:
        print booking.client
    # for booking in Booking.objects.all():
    #     print booking.arrive_time
    # print "now " + str((timezone.now() + datetime.timedelta(hours=1)))
    # print timezone.now()
    # print to_see
    return HttpResponse(bookings_to_assigned[0].client)
