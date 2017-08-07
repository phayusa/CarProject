from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Information for a person as driver or client
class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mail = models.EmailField(blank=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.last_name + ' ' + self.first_name


# Client information
class Client(Person):
    payment = models.CharField(max_length=5)


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
        return self.model


# One travel did by multiples clients link to one car
class Travel(models.Model):
    departure = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    car = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.destination


# One booking made by a client
class Booking(models.Model):
    date = models.DateField(auto_now=True)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, null=True)

    # Information about persons
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    passengers = models.IntegerField()
    luggage_number = models.IntegerField()

    # Flight info
    flight = models.CharField(max_length=200)
    arrive_time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.date.strftime('%m/%d/%Y')+' '+self.travel.destination


# Driver information
class Driver(Person):
    revenues = models.IntegerField()
    remuneration = models.IntegerField()
