from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Back_Source.models import Client, BuissnessPartner, Commercial, Operator, Driver
from Back_Source.serializers import ClientSerializer


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
            if BuissnessPartner.objects.filter(user=self.request.user).exists() or Operator.objects.filter(
                    user=self.request.user).exists():
                return Client.objects.filter(partner__user=self.request.user)
            else:
                if Commercial.objects.filter(user=self.request.user).exists():
                    commercial = Commercial.objects.filter(user=self.request.user)[0]
                    return Client.objects.filter(partner=commercial.partner)
                else:
                    return None
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


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer

    redirect_unauthenticated_users = False
    authentication_classes = [JSONWebTokenAuthentication, ]
    raise_exception = True

    def get_queryset(self):
        if not self.request.user.is_superuser:
            if BuissnessPartner.objects.filter(user=self.request.user).exists() or Operator.objects.filter(
                    user=self.request.user).exists():
                return Client.objects.filter(partner__user=self.request.user)
            else:
                if Commercial.objects.filter(user=self.request.user).exists():
                    commercial = Commercial.objects.filter(user=self.request.user)[0]
                    return Client.objects.filter(partner=commercial.partner)
                else:
                    if Driver.objects.filter(user=self.request.user):
                        return Client.objects.all()
                    else:
                        return None
        return Client.objects.all()