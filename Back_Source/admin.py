from django.contrib import admin

from Back_Source.models import *


class VehicleAdmin(admin.ModelAdmin):
    model = Vehicle
    radio_fields = {"area": admin.VERTICAL}
    list_display = ('registration', 'travelling', 'empty_places', 'empty_luggages', 'revenues')
    list_filter = ('model__name', 'model__number_place', 'model__child_seat')
    # readonly_fields = ('travelling',)


class BookingAdmin(admin.ModelAdmin):
    model = Booking
    list_display = ('date', 'client', 'airport', 'destination', 'flight', 'arrive_time', 'status')
    search_fields = ('client__first_name', 'client__last_name', 'flight', 'arrive_time', 'status')
    list_filter = ('date', 'arrive_time', 'status')
    ordering = ('date',)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'mail', 'phone_number')
    search_fields = ('first_name', 'last_name', 'mail')
    list_filter = ('gender',)
    ordering = ('first_name', 'last_name')


class DriverAdmin(PersonAdmin):
    list_display = ('first_name', 'last_name', 'mail', 'phone_number', 'revenues')


class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'child_seat', 'number_place', 'luggage_number', 'price')
    list_filter = ('number_place', 'name', 'child_seat')


class TravelAdmin(admin.ModelAdmin):
    ordering = ('start', 'done')
    list_filter = ('start', 'airport', 'area', 'done')
    list_display = ('start', 'end', 'airport', 'area', 'done')


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'north', 'south', 'east', 'west')


admin.site.register(Client, PersonAdmin)
admin.site.register(Commercial, PersonAdmin)
admin.site.register(BuissnessPartner, PersonAdmin)
admin.site.register(Operator, PersonAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Travel, TravelAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingPartner)
admin.site.register(BookingCommecial)
admin.site.register(BookingOperator)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Airport)
admin.site.register(VehicleModel, VehicleModelAdmin)
