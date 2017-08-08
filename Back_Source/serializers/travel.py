from rest_framework import serializers
from Back_Source.models.travel import Travel


class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        fields = '__all__'

