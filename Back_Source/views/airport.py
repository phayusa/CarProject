from braces.views import RecentLoginRequiredMixin
from rest_framework import generics

from Back_Source.models import Airport
from Back_Source.permissions.person import ClientPermission
from Back_Source.serializers import AirportSerializer

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


class AirportBase(generics.GenericAPIView):
    # Require a login within the last 10 minutes
    # max_last_login_delta = 60000

    serializer_class = AirportSerializer
    # redirect_unauthenticated_users = False
    # permission_classes = (ClientPermission, )
    permission_classes = (IsAuthenticated,)

    # authentication_classes = (JSONWebTokenAuthentication, )
    # raise_exception = True

    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return Airport.objects.filter(client=Airport.objects.filter(user=self.request.user))
        return Airport.objects.all()


class AirportList(AirportBase, generics.ListAPIView):
    pass
    # filter_fields = ('date', 'travel', 'client')


class AirportCreate(AirportBase, generics.CreateAPIView):
    pass


class AirportDetail(AirportBase, generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    # redirect_field_name = '.'
