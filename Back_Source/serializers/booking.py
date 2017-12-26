from Back_Source.models.booking import Booking, BookingCommecial, BookingPartner, BookingOperator
from rest_framework import serializers


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingCommercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingCommecial
        fields = '__all__'


class BookingOperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingOperator
        fields = '__all__'


class BookingPartenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPartner
        fields = '__all__'
