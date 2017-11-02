from django.db import models
from person import Client
from vehicle import Vehicle
from geoposition.fields import GeopositionField


# One booking made by a client
class Booking(models.Model):
    departure = GeopositionField()
    destination = GeopositionField()

    date = models.DateField(auto_now=True)
    # travel = models.ForeignKey(Travel, on_delete=models.CASCADE, null=True)

    # Information about persons
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    passengers = models.IntegerField()
    luggage_number = models.IntegerField()

    # Flight info
    flight = models.CharField(max_length=200)
    arrive_time = models.DateTimeField(blank=True)

    # Processing value
    vehicle_choose = models.ForeignKey(Vehicle, blank=True, null=True)
    # To know the nth booking selected for the travel
    distance = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.client) + ' ' + self.date.strftime('%m/%d/%Y') + ' for ' + self.arrive_time.strftime(
            '%m/%d/%Y %Hh%M')
