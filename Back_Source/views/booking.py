from braces.views import RecentLoginRequiredMixin
from rest_framework import generics

from Back_Source.models import Booking, Client
from Back_Source.permissions.person import ClientPermission
from Back_Source.serializers import BookingSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class BookingBase(RecentLoginRequiredMixin, generics.GenericAPIView):
    # Require a login within the last 10 minutes
    max_last_login_delta = 600

    serializer_class = BookingSerializer
    redirect_unauthenticated_users = False
    permission_classes = (ClientPermission, )
    authentication_classes = (JSONWebTokenAuthentication, )
    raise_exception = True

    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return Booking.objects.filter(client=Client.objects.filter(user=self.request.user))
        return Booking.objects.all()


class BookingList(BookingBase, generics.ListAPIView):
    filter_fields = ('date', 'travel', 'client')


class BookingCreate(BookingBase, generics.CreateAPIView):
    pass


class BookingDetail(BookingBase, generics.RetrieveUpdateDestroyAPIView):
    pass
    # redirect_field_name = '.'

