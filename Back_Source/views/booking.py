from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from Back_Source.models import Booking, Client, BookingPartner, BookingCommecial, BuissnessPartner, Commercial
from Back_Source.models import BookingOperator
from Back_Source.serializers import BookingOperatorSerializer
from Back_Source.serializers import BookingSerializer, BookingCommercialSerializer, BookingPartenerSerializer


# class BookingBase(RecentLoginRequiredMixin, generics.GenericAPIView):
class BookingBase(generics.GenericAPIView):
    # Require a login within the last 10 minutes
    # max_last_login_delta = 900

    serializer_class = BookingSerializer
    redirect_unauthenticated_users = False
    # permission_classes = (ClientPermission, )
    permission_classes = (IsAuthenticated,)
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


class BookingCommecialBase(generics.GenericAPIView):
    # Require a login within the last 10 minutes
    # max_last_login_delta = 900

    serializer_class = BookingCommercialSerializer
    redirect_unauthenticated_users = False
    # permission_classes = (ClientPermission, )
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, )
    raise_exception = True

    def get_queryset(self):
        if not self.request.user.is_superuser:
            if BuissnessPartner.objects.filter(user=self.request.user).exists():
                return BookingCommecial.objects.filter(commercial__partner__user=self.request.user)
            else:
                if Commercial.objects.filter(user=self.request.user).exists():
                    return BookingCommecial.objects.filter(commercial__user=self.request.user)
                else:
                    return None
        return BookingCommecial.objects.all()
        # if self.request.user.groups.filter(name='Clients').exists():
        #     return BookingCommecial.objects.filter(client=Client.objects.filter(user=self.request.user))
        # return BookingCommecial.objects.all()


class BookingCommercialList(BookingCommecialBase, generics.ListAPIView):
    filter_fields = ('date', 'travel', 'client')


class BookingPartenerBase(generics.GenericAPIView):
    # Require a login within the last 10 minutes
    # max_last_login_delta = 900

    serializer_class = BookingPartenerSerializer
    redirect_unauthenticated_users = False
    # permission_classes = (ClientPermission, )
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, )
    raise_exception = True

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return BookingPartner.objects.filter(partner__user=self.request.user)
        return BookingPartner.objects.all()
        # if self.request.user.groups.filter(name='Clients').exists():
        #     return BookingPartner.objects.filter(client=Client.objects.filter(user=self.request.user))
        # return BookingPartner.objects.all()


class BookingPartenerList(BookingPartenerBase, generics.ListAPIView):
    filter_fields = ('date', 'travel', 'client')


class BookingOperatorBase(generics.GenericAPIView):
    # Require a login within the last 10 minutes
    # max_last_login_delta = 900

    serializer_class = BookingOperatorSerializer
    redirect_unauthenticated_users = False
    # permission_classes = (ClientPermission, )
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (JSONWebTokenAuthentication, )
    raise_exception = True

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return BookingOperator.objects.filter(operator__user=self.request.user)
        return BookingOperator.objects.all()
        # if self.request.user.groups.filter(name='Clients').exists():
        #     return BookingPartner.objects.filter(client=Client.objects.filter(user=self.request.user))
        # return BookingPartner.objects.all()


class BookingOperatorList(BookingOperatorBase, generics.ListAPIView):
    filter_fields = ('date', 'client')
