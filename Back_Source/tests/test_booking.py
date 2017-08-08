# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from Back_Source.models import Client, Vehicle, Travel, Booking


class OneBookingTestCase(TestCase):

    def test_booking(self):
        # create_car
        self.vehicle = Vehicle(brand="Peugeot",model="508")
        self.vehicle.year = "2015"
        self.vehicle.color = "black"
        self.vehicle.category = "sedan"
        self.vehicle.registration = "AT-589-97"

        self.vehicle.child_seat = False
        self.vehicle.number_place = 5
        self.vehicle.luggage_number = 15

        self.assertIs(str(self.vehicle) == "Peugeot 508", True)

        # Test the creation of the client
        self.client = Client(first_name="Delacroix", last_name="Jean Pierre")
        self.client.age = 20
        self.client.gender = "male"
        self.client.mail = "Delacroix.Jp@gmail.com"
        self.client.phone_number = "+33625479512"
        self.client.payment = "CB"
        self.assertIs(str(self.client) == "Jean Pierre Delacroix", True)

        # Create the travel wanted by the client
        self.travel = Travel(departure="Aéroport Charles de Gaules", destination="16 rue du bois jolie, 75015")
        self.travel.car = self.vehicle
        self.assertIs(self.vehicle, self.travel.car)

        # Create the booking for the client when it choose it's travel
        self.booking = Booking(date=timezone.now(), travel=self.travel, client=self.client)
        self.booking.passengers = 4
        self.booking.luggage_number = 10
        self.booking.flight = "10174865744125300"
        self.booking.arrive_time = timezone.now()
        self.assertIs(self.booking.travel, self.travel)




