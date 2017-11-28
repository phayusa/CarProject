from Back_Source.models.location import Airport
from rest_framework import serializers


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'
