from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import generics

from Back_Source.models import Client
from Back_Source.permissions.person import ClientPermission
from Back_Source.serializers import ClientSerializer


# Base view for all client manipulations with restrictions
class ClientBase(generics.GenericAPIView):
    serializer_class = ClientSerializer

    redirect_unauthenticated_users = False
    permission_classes = [ClientPermission, ]
    raise_exception = True

    # Return only the booking of the connected client
    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return Client.objects.filter(user=self.request.user)
        return Client.objects.all()


class ClientList(ClientBase, generics.ListAPIView):
    pass


class ClientCreate(ClientBase, generics.CreateAPIView):

    def perform_create(self, serializer):
        queryset = User.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError('You have already signed up')
        serializer.save(user=self.request.user)


class ClientDetail(ClientBase, generics.RetrieveUpdateDestroyAPIView):
    pass




