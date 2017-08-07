from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    mail = models.EmailField()


class Client(Person):
    payment = models.CharField(max_length=5)


class Car(models.Model):
    number_place = models.IntegerField()
    model = models.CharField(max_length=200)


class Travel(models.Model):
    destination = models.CharField(max_length=500)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)


class Booking(models.Model):
    name = models.CharField(max_length=20)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, null=True)
