from django.db import models
from vehicle import Vehicle
from person import Driver


# One travel did by multiples clients link to one car
class Travel(models.Model):
    departure = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    car = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.destination
