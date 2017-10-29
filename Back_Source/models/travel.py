from django.db import models
from vehicle import Vehicle
from person import Driver


# One travel did by multiples clients link to one car
class Travel(models.Model):
    departure = models.CharField(max_length=500)
    destination = models.CharField(max_length=500)
    car = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)

    # Fill before and before the travel
    start = models.DateField()
    end = models.DateField()

    def __unicode__(self):
        return u'%s - %s' % (self.departure, self.destination)
