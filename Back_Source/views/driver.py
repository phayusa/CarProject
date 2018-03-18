# -*- coding: utf-8 -*-

from django.http import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Back_Source.models import Vehicle, Driver, Travel
from Back_Source.permissions.person import DriverPermission
from Back_Source.serializers import DriverSerializer, BookingSerializer


class DriverBase(generics.GenericAPIView):
    serializer_class = DriverSerializer

    # redirect_unauthenticated_users = False
    # authentication_classes = [JSONWebTokenAuthentication, ]
    # raise_exception = True

    # Return only the booking of the connected client
    def get_queryset(self):
        if self.request.user.groups.filter(name='Drivers').exists():
            return Driver.objects.filter(user=self.request.user)
        return Driver.objects.all()


class DriverList(DriverBase, generics.ListAPIView):
    pass


class DriverDetail(DriverBase, generics.CreateAPIView):
    pass


class DriverCreate(DriverBase, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = IsAdminUser


# Check if we are on mobile
def is_mobile_app_access(request):
    return request.META.get('HTTP_REFERER', None) is None and request.META.get('HTTP_COOKIE',
                                                                               None) is None and request.META.get(
        'HTTP_X_REQUESTED_WITH', None) == 'your.app.name.here' and request.META.get('HTTP_ORIGIN', None) == 'file://'


@method_decorator(csrf_exempt, name="dispatch")
class DriverBookings(APIView):
    permission_classes = [DriverPermission, ]
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    def get(self, request, **kwargs):
        try:
            if not request.user:
                return HttpResponse("[]")
            drivers = Driver.objects.filter(user=request.user)
            if not drivers:
                return HttpResponse("[]")
            driver = drivers[0]
            vehicles = Vehicle.objects.filter(driver=driver)
            if not vehicles:
                return HttpResponse("[]")
            vehicle = vehicles[0]
            travels = Travel.objects.filter(car=vehicle, start=None)
            if not travels:
                return HttpResponse("[]")
            travel = travels[0]
            if not travel.driver:
                travel.driver = driver
                travel.save()
            serialize = BookingSerializer(travel.bookings.all(), many=True)
            return HttpResponse(JSONRenderer().render(serialize.data))
            # return HttpResponse(json.dumps(travel.bookings.order_by('distance')))
        except IndexError:
            return HttpResponse("Bad Request")
