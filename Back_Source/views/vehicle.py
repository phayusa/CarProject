from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from Back_Source.models import Vehicle, Driver
from Back_Source.permissions.person import DriverPermission
from Back_Source.serializers import VehicleSerializer


class VehicleBase(generics.GenericAPIView):

    serializer_class = VehicleSerializer
    redirect_unauthenticated_users = False
    permission_classes = [DriverPermission, ]
    raise_exception = True

    # Return only the booking of the connected client
    def get_queryset(self):
        if self.request.user.groups.filter(name='Drivers').exists():
            return Vehicle.objects.filter(driver=Driver.objects.filter(user=self.request.user))
        return Vehicle.objects.all()


class VehicleList(VehicleBase, generics.ListAPIView):
    pass


class VehicleCreate(VehicleBase, generics.CreateAPIView):
    permission_classes = IsAdminUser


class VehicleDetail(VehicleBase, generics.RetrieveUpdateDestroyAPIView):
    pass

