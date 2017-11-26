from rest_framework import serializers
from Back_Source.models.person import Client, Driver, Commercial, BuissnessPartner


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class CommercialSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = Commercial
        fields = '__all__'


class PartenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuissnessPartner
        fields = '__all__'
