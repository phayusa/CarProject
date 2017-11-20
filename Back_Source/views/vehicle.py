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

from rest_framework.renderers import JSONRenderer

class VehicleBase(generics.GenericAPIView):
    serializer_class = VehicleSerializer
    redirect_unauthenticated_users = False
    permission_classes = [DriverPermission, ]
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    # Return only the booking of the connected client
    def get_queryset(self):
        if self.request.user.groups.filter(name='Drivers').exists():
            return Vehicle.objects.filter(driver=Driver.objects.filter(user=self.request.user))
        return Vehicle.objects.all()


class VehicleModelBase(generics.GenericAPIView):
    serializer_class = VehicleModelSerializer
    permission_classes = [GeneralPermission, ]
    queryset = VehicleModel.objects.all()


class VehicleModelList(VehicleModelBase, generics.ListAPIView):
    pass


class VehicleList(VehicleBase, generics.ListAPIView):
    pass


class VehicleCreate(VehicleBase, generics.CreateAPIView):
    permission_classes = IsAdminUser


class VehicleDetail(VehicleBase, generics.RetrieveUpdateDestroyAPIView):
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


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


@method_decorator(csrf_exempt, name="dispatch")
class VehicleDriverSetter(APIView):
    permission_classes = [DriverPermission, ]
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    def get(self, request, pk, **kwargs):
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
