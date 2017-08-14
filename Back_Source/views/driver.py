from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from Back_Source.models import Driver
from Back_Source.permissions.person import DriverPermission
from Back_Source.serializers import DriverSerializer


class DriverBase(generics.GenericAPIView):
    serializer_class = DriverSerializer

    redirect_unauthenticated_users = False
    permission_classes = [DriverPermission, ]
    raise_exception = True

    # Return only the booking of the connected client
    def get_queryset(self):
        if self.request.user.groups.filter(name='Drivers').exists():
            return Driver.objects.filter(user=self.request.user)
        return Driver.objects.all()


class DriverList(DriverBase):
    pass


class DriverDetail(DriverBase):
    pass


class DriverCreate(DriverBase):
    permission_classes = IsAdminUser
