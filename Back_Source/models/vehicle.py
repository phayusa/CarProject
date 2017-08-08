from django.db import models


# Vehicle information
class Vehicle(models.Model):
    # std fields
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100)
    registration = models.CharField(max_length=9)

    # Seats fields
    child_seat = models.BooleanField()
    number_place = models.IntegerField()
    luggage_number = models.IntegerField()

    # Position fields
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)

    # File or photos to upload
    insurance = models.FileField()
    insurance_card = models.FileField()
    registration_card = models.FileField()
    front = models.ImageField()
    back = models.ImageField()

    # Buisness field
    revenues = models.IntegerField()

    def __str__(self):
        return self.brand + ' '+self.model
