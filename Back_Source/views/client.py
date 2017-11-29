from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Back_Source.models import Client
from Back_Source.permissions.person import ClientPermission
from Back_Source.serializers import ClientSerializer
from rest_framework.renderers import JSONRenderer

from django.http import HttpResponse

import json


# Base view for all client manipulations with restrictions
class ClientBase(generics.GenericAPIView):
    serializer_class = ClientSerializer

    # redirect_unauthenticated_users = False
    # permission_classes = [ClientPermission, ]
    # authentication_classes = [JSONWebTokenAuthentication, ]
    # raise_exception = True

    # Return only the booking of the connected client
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Client.objects.filter(partner__user=self.request.user)
        return Client.objects.all()


class ClientList(ClientBase, generics.ListAPIView):
    pass

# def ClientList(request):
#     clientsSerialize = ClientSerializer(Client.objects.all(), many=True)
#     json_ser = JSONRenderer().render(clientsSerialize.data)
#     final = {}
#     final["aaData"] = json_ser
#     return HttpResponse(json.dumps(final), content_type="application/json")


class ClientCreate(ClientBase, generics.CreateAPIView):
    def perform_create(self, serializer):
        queryset = User.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError('You have already signed up')
        serializer.save(user=self.request.user)


class ClientDetail(ClientBase, generics.RetrieveUpdateDestroyAPIView):
    pass
