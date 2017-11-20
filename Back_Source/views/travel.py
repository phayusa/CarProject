from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Back_Source.models import Travel, Driver
from Back_Source.permissions.person import DriverPermission, ClientPermission
from Back_Source.serializers import TravelSerializer


class TravelBase(generics.GenericAPIView):
    serializer_class = TravelSerializer

    redirect_unauthenticated_users = False
    permission_classes = [DriverPermission, ClientPermission]
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    # Return only the booking of the connected client
    def get_queryset(self):
        if self.request.user.groups.filter(name='Drivers').exists():
            return Travel.objects.filter(driver=Driver.objects.filter(user=self.request.user))
        return Travel.objects.all()


@method_decorator(csrf_exempt, name="dispatch")
class TravelList(TravelBase, generics.ListCreateAPIView):

    def get_queryset(self):
        if self.request.user.groups.filter(name='Drivers').exists():
            return Travel.objects.filter(driver=Driver.objects.filter(user=self.request.user))
        return Travel.objects.all()


class TravelCreate(TravelBase, generics.CreateAPIView):
    pass


class TravelDetail(TravelBase, generics.RetrieveUpdateDestroyAPIView):
    pass
