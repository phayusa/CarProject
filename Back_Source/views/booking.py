from braces.views import RecentLoginRequiredMixin
from rest_framework import generics

from Back_Source.models import Booking, Client, BookingPartner, BookingCommecial
from Back_Source.permissions.person import ClientPermission
from Back_Source.serializers import BookingSerializer, BookingCommercialSerializer, BookingPartenerSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BookingBase(RecentLoginRequiredMixin, generics.GenericAPIView):
    # Require a login within the last 10 minutes
    max_last_login_delta = 900

    serializer_class = BookingSerializer
    redirect_unauthenticated_users = False
    # permission_classes = (ClientPermission, )
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (JSONWebTokenAuthentication, )
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


class BookingCommecialBase(RecentLoginRequiredMixin, generics.GenericAPIView):
    # Require a login within the last 10 minutes
    max_last_login_delta = 900

    serializer_class = BookingCommercialSerializer
    redirect_unauthenticated_users = False
    # permission_classes = (ClientPermission, )
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (JSONWebTokenAuthentication, )
    raise_exception = True

    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return BookingCommecial.objects.filter(client=Client.objects.filter(user=self.request.user))
        return BookingCommecial.objects.all()


class BookingCommercialList(BookingCommecialBase, generics.ListAPIView):
    filter_fields = ('date', 'travel', 'client')


class BookingPartenerBase(RecentLoginRequiredMixin, generics.GenericAPIView):
    # Require a login within the last 10 minutes
    max_last_login_delta = 900

    serializer_class = BookingPartenerSerializer
    redirect_unauthenticated_users = False
    # permission_classes = (ClientPermission, )
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (JSONWebTokenAuthentication, )
    raise_exception = True

    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return BookingPartner.objects.filter(client=Client.objects.filter(user=self.request.user))
        return BookingPartner.objects.all()


class BookingPartenerList(BookingPartenerBase, generics.ListAPIView):
    filter_fields = ('date', 'travel', 'client')



