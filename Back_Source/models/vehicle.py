from django.db import models
from person import Driver
from area import Area
from geoposition.fields import GeopositionField


class VehicleModel(models.Model):
    # Classical attributes
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.CharField(max_length=4)

    # Seats fields
    child_seat = models.BooleanField()
    number_place = models.IntegerField()
    luggage_number = models.IntegerField()

    # Category of the vehicle
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category + ' : ' + self.brand + ' ' + self.model + ' ' + str(self.year)


# Vehicle information
class Vehicle(models.Model):
    # Model
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)

    # Driver of the car
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, null=True, blank=True)

    # std fields
    registration = models.CharField(max_length=9)
    color = models.CharField(max_length=100, null=True)

    # Position fields
    pos = GeopositionField(blank=True)

    # File or photos to upload
    insurance = models.FileField()
    insurance_card = models.FileField()
    registration_card = models.FileField()
    front = models.ImageField()
    back = models.ImageField()

    # Buisness field
    revenues = models.IntegerField(blank=True, null=True)

    # Processing attributes
    # Busy car
    empty_places = models.IntegerField()
    empty_luggages = models.IntegerField()
    travelling = models.BooleanField(default=False, blank=True)

    # Link area to car
    area = models.ForeignKey(Area, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.registration
