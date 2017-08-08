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


# Driver information
class Driver(Person):
    revenues = models.IntegerField()
    remuneration = models.IntegerField()