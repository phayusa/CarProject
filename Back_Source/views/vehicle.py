import datetime

from django.conf import settings
from django.http import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Back_Source.models import Vehicle, Driver, VehicleModel
from Back_Source.permissions.person import DriverPermission, GeneralPermission
from Back_Source.serializers import VehicleSerializer, VehicleModelSerializer
from ..models import Travel
from geoposition import Geoposition


class VehicleBase(generics.GenericAPIView):
    serializer_class = VehicleSerializer

    # Return only the booking of the connected client
    def get_queryset(self):
        drivers = Driver.objects.filter(user=self.request.user)
        if drivers:
            driver = drivers[0]

            car = Vehicle.objects.filter(driver=driver)
            if not car:
                return Vehicle.objects.filter(travelling=False)
            return car

        if self.request.user.is_superuser:
            return Vehicle.objects.all()
        return None


class VehicleModelBase(generics.GenericAPIView):
    serializer_class = VehicleModelSerializer
    permission_classes = [GeneralPermission, ]
    queryset = VehicleModel.objects.all()


class VehicleModelList(VehicleModelBase, generics.ListAPIView):
    pass


class VehicleListJson(VehicleBase, generics.ListAPIView):
    redirect_unauthenticated_users = False
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True


class VehicleList(VehicleBase, generics.ListAPIView):
    pass


class VehicleCreate(VehicleBase, generics.CreateAPIView):
    permission_classes = IsAdminUser


class VehicleDetail(VehicleBase, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleSerializer
    redirect_unauthenticated_users = False
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

        # def partial_update(self, request, *args, **kwargs):
        #     kwargs['partial'] = True
        #     return self.update(request, *args, **kwargs)


def serve_image(request, image):
    try:
        with open(settings.MEDIA_ROOT + "/" + image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        return HttpResponse("None")
        # red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        # response = HttpResponse(content_type="image/jpeg")
        # red.save(response, "JPEG")
        # return response


def serve_vehicle_driver(request, pk):
    try:
        driver = Driver.objects.filter(user=request.user)[0]
        if not driver:
            return HttpResponse("Bad Request")
        vehicle = Vehicle.objects.filter(id=pk)[0]
        if not vehicle:
            return HttpResponse("Bad Request")
        vehicle.driver = driver
        vehicle.save()
        return HttpResponse("Ok")
    except IndexError:
        return HttpResponse("Bad Request")


# Check if we are on mobile
def is_mobile_app_access(request):
    return request.META.get('HTTP_REFERER', None) is None and request.META.get('HTTP_COOKIE',
                                                                               None) is None and request.META.get(
        'HTTP_X_REQUESTED_WITH', None) == 'your.app.name.here' and request.META.get('HTTP_ORIGIN', None) == 'file://'


@method_decorator(csrf_exempt, name="dispatch")
class VehicleDriverSetter(APIView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    def get(self, request, pk, **kwargs):
        try:
            # if not is_mobile_app_access(request):
            #     return HttpResponse("Bad Request")
            driver = Driver.objects.filter(user=request.user)[0]
            if not driver:
                return HttpResponse("Bad Request")
            vehicle = Vehicle.objects.filter(id=pk)[0]
            if not vehicle:
                return HttpResponse("Bad Request")
            vehicle.driver = driver
            vehicle.save()

            travels = Travel.objects.filter(car=vehicle, done=False, end__gt=datetime.datetime.now(),
                                            start__gt=datetime.datetime.now())
            for travel in travels:
                travel.driver = driver
                travel.save()
            return HttpResponse("Ok")
        except IndexError:
            return HttpResponse("Bad Request")

    def post(self, request, pk, **kwargs):
        try:
            # if not is_mobile_app_access(request):
            #     return HttpResponse("Bad Request")
            driver = Driver.objects.filter(user=request.user)[0]
            if not driver:
                return HttpResponse("Bad Request")
            vehicle = Vehicle.objects.filter(id=pk)[0]
            if not vehicle:
                return HttpResponse("Bad Request")
            vehicle.driver = None
            vehicle.save()

            travels = Travel.objects.filter(car=vehicle, done=False, end__gt=datetime.datetime.now(),
                                            start__gt=datetime.datetime.now())
            for travel in travels:
                travel.driver = None
                travel.save()
            return HttpResponse("Ok")
        except IndexError:
            return HttpResponse("Bad Request")
