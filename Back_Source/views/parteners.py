from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import generics

from Back_Source.models import BuissnessPartner
from Back_Source.serializers import PartenerSerializer


# Base view for all client manipulations with restrictions
class PartenerBase(generics.GenericAPIView):
    serializer_class = PartenerSerializer

    # redirect_unauthenticated_users = False
    # permission_classes = [ClientPermission, ]
    # authentication_classes = [JSONWebTokenAuthentication, ]
    # raise_exception = True

    # Return only the booking of the connected Commercial
    def get_queryset(self):
        if self.request.user.groups.filter(name='Clients').exists():
            return BuissnessPartner.objects.filter(user=self.request.user)
        return BuissnessPartner.objects.all()


class PartenerList(PartenerBase, generics.ListAPIView):
    pass

# def ClientList(request):
#     clientsSerialize = ClientSerializer(Commercial.objects.all(), many=True)
#     json_ser = JSONRenderer().render(clientsSerialize.data)
#     final = {}
#     final["aaData"] = json_ser
#     return HttpResponse(json.dumps(final), content_type="application/json")


class PartenerCreate(PartenerBase, generics.CreateAPIView):
    def perform_create(self, serializer):
        queryset = User.objects.filter(user=self.request.user)
        if queryset.exists():
            raise ValidationError('You have already signed up')
        serializer.save(user=self.request.user)


class PartenerDetail(PartenerBase, generics.RetrieveUpdateDestroyAPIView):
    pass
