from braces.views import RecentLoginRequiredMixin
from rest_framework import generics

from Back_Source.models import Booking, Client
from Back_Source.permissions.booking import BookingPermissions
from Back_Source.serializers import BookingSerializer


class BookingList(RecentLoginRequiredMixin, generics.ListAPIView):
    # Require a login within the last 10 minutes
    max_last_login_delta = 600

    serializer_class = BookingSerializer
    redirect_unauthenticated_users = False
    permission_classes = [BookingPermissions, ]
    raise_exception = True
    filter_fields = ('date', 'travel', 'client')

    # Return only the booking of the connected client
    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return Booking.objects.filter(client=Client.objects.filter(user=self.request.user))
        return Booking.objects.all()


class BookingDetail(RecentLoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    # Require a login within the last 10 minutes
    max_last_login_delta = 600

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [BookingPermissions, ]
    redirect_field_name = '.'
    redirect_unauthenticated_users = False
    raise_exception = True
