from django.db import models
from vehicle import Vehicle
from person import Driver, Client
from booking import Booking


# One travel did by multiples clients link to one car
class Travel(models.Model):
    car = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)

    # Fill during the attribution of driver
    bookings = models.ManyToManyField(Booking, blank=True)

    # Fill before and before the travel
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.car, self.driver)
