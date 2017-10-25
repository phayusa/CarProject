from django.contrib import admin

# Register your models here.
from Back_Source.models import *

admin.site.register(Client)
admin.site.register(Vehicle)
admin.site.register(Travel)
admin.site.register(Booking)
admin.site.register(Driver)
admin.site.register(Area)
