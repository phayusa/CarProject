from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Back_Source.models import Travel, Driver, Vehicle
from Back_Source.permissions.person import DriverPermission, ClientPermission
from Back_Source.serializers import TravelSerializer
from django.utils import timezone
from django.http import *


class TravelBase(generics.GenericAPIView):
    serializer_class = TravelSerializer

    redirect_unauthenticated_users = False
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    # Return only the booking of the connected client
    def get_queryset(self):
        if self.request.user.groups.filter(name='Drivers').exists():
            return Travel.objects.filter(driver=Driver.objects.filter(user=self.request.user))
        return Travel.objects.all()


# # Check if we are on mobile
# def is_mobile_app_access(request):
#     return request.META.get('HTTP_REFERER', None) is None and request.META.get('HTTP_COOKIE',
#                                                                                None) is None and request.META.get(
#         'HTTP_X_REQUESTED_WITH', None) == 'your.app.name.here' and request.META.get('HTTP_ORIGIN', None) == 'file://'
#

@method_decorator(csrf_exempt, name="dispatch")
class TravelList(TravelBase, generics.ListCreateAPIView):
    def get_queryset(self):
        # if not is_mobile_app_access(self.request):
        #     return HttpResponse("[]")
        # if not self.request.user.is_authentificated:
        #     return '[]'

        drivers = Driver.objects.filter(user=self.request.user)
        if drivers:
            car = Vehicle.objects.filter(driver=drivers[0])
            # return Travel.objects.filter(car=car,
            #                              start__day=timezone.now().day)
            return Travel.objects.filter(car=car)
        if self.request.user.is_superuser:
            return Travel.objects.all()
        return None


class TravelCreate(TravelBase, generics.CreateAPIView):
    pass


class TravelDetail(TravelBase, generics.RetrieveUpdateDestroyAPIView):
    pass
