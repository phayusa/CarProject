# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from Back_Source.models import Client, Travel, Booking, Area, Driver, Vehicle, VehicleModel
from Localisation.views import get_area, upload_bookings_vehicle, end_driver


class SetterAreaTestCase(TestCase):
    def setUp(self):
        self.high_left = Area(name="HighLeft", north=48.9436905964, south=48.8615431088, east=2.34387235449,
                              west=2.13101286719)
        self.high_right = Area(name="HighRight", north=48.9436905964, south=48.8615431088, east=2.55947904395,
                               west=2.34490294287)
        self.bottom_left = Area(name="BottomLeft", north=48.8613172129, south=48.7493884293, east=2.34318570898,
                                west=2.13032622168)
        self.bottom_right = Area(name="BottomRight", north=48.8608654779, south=48.748935685, east=2.55810575293,
                                 west=2.34524626563)

        self.high_left.save()
        self.high_right.save()
        self.bottom_left.save()
        self.bottom_right.save()

        self.user = User.objects.create_user(username='Letest',
                                             email='jlennon@beatles.com',
                                             password='glass onion')

        self.client = Client(first_name="Test", last_name="Client")
        self.client.age = 32
        self.client.gender = "male"
        self.client.phone_number = "+33612547852"
        self.client.user = self.user
        # self.client.save()

    def test_area_bottom_left(self):
        # client.user =

        travel = Travel()

        # create booking
        booking = Booking()
        booking.travel = travel
        booking.client = self.client
        booking.passengers = 1
        booking.luggage_number = 2
        booking.flight = "18070-12324"
        booking.departure = "Aéroport Charles de Gaulle (T3-Roissypole), Tremblay-en-France"
        booking.destination = "Champ de Mars, 5 Avenue Anatole France, 75007 Paris"

        self.assertFalse(booking is None)
        self.assertFalse(booking.travel is None)

        self.assertEqual(get_area(booking), self.bottom_left)

    def test_area_high_left(self):
        travel = Travel()

        # create booking
        booking = Booking()
        booking.travel = travel
        booking.client = self.client
        booking.passengers = 1
        booking.luggage_number = 2
        booking.flight = "18070-12324"
        booking.departure = "Aéroport Charles de Gaulle (T3-Roissypole), Tremblay-en-France"
        booking.destination = "Place Charles de Gaulle, 75008 Paris"

        self.assertFalse(booking is None)
        self.assertFalse(booking.travel is None)

        self.assertEqual(get_area(booking), self.high_left)

    def test_area_high_right(self):
        travel = Travel()

        # create booking
        booking = Booking()
        booking.travel = travel
        booking.client = self.client
        booking.passengers = 1
        booking.luggage_number = 2
        booking.flight = "18070-12324"
        booking.departure = "Aéroport Charles de Gaulle (T3-Roissypole), Tremblay-en-France"
        booking.destination = "23 Rue Madeleine Vionnet, 93300 Aubervilliers"

        self.assertFalse(booking is None)
        self.assertFalse(booking.travel is None)

        self.assertEqual(get_area(booking), self.high_right)

    def test_area_bottom_right(self):
        travel = Travel()
        travel.departure = "Aéroport Charles de Gaulle (T3-Roissypole), Tremblay-en-France"
        travel.destination = "Place de la Libération, 94400 Vitry-sur-Seine"

        # create booking
        booking = Booking()
        booking.travel = travel
        booking.client = self.client
        booking.passengers = 1
        booking.luggage_number = 2
        booking.flight = "18070-12324"

        self.assertFalse(booking is None)
        self.assertFalse(booking.travel is None)

        self.assertEqual(get_area(booking), self.bottom_right)


class SetterVehicleBookingTestCase(TestCase):
    def setUp(self):
        self.high_left = Area(name="HighLeft", north=48.9436905964, south=48.8615431088, east=2.34387235449,
                              west=2.13101286719)
        self.high_right = Area(name="HighRight", north=48.9436905964, south=48.8615431088, east=2.55947904395,
                               west=2.34490294287)
        self.bottom_left = Area(name="BottomLeft", north=48.8613172129, south=48.7493884293, east=2.34318570898,
                                west=2.13032622168)
        self.bottom_right = Area(name="BottomRight", north=48.8608654779, south=48.748935685, east=2.55810575293,
                                 west=2.34524626563)

        self.high_left.save()
        self.high_right.save()
        self.bottom_left.save()
        self.bottom_right.save()

        self.user = User.objects.create_user(username='Letest',
                                             email='jlennon@beatles.com',
                                             password='glass onion')

        self.client = Client(first_name="Test", last_name="Client")
        self.client.age = 32
        self.client.gender = "male"
        self.client.phone_number = "+33612547852"
        self.client.user = self.user

        self.client.save()

        self.travel = Travel()
        self.travel.departure = "Aéroport Charles de Gaulle (T3-Roissypole), Tremblay-en-France"
        self.travel.destination = "Champ de Mars, 5 Avenue Anatole France, 75007 Paris"

        self.travel.save()

        # create booking
        self.booking = Booking()
        self.booking.travel = self.travel
        self.booking.client = self.client
        self.booking.passengers = 1
        self.booking.luggage_number = 2
        self.booking.flight = "18070-12324"
        self.booking.arrive_time = timezone.now() + datetime.timedelta(minutes=1)

        self.booking.save()

        self.userB = User.objects.create_user(username='Chauffeur du dimanche',
                                              email='jlennon@beatles.com',
                                              password='glass onion')

        # create driver
        self.driver = Driver()
        self.driver.age = 45
        self.driver.gender = "female"
        self.driver.phone_number = "+33612547852"
        self.driver.user = self.userB
        self.driver.save()

        self.booking.save()

        model, _ = VehicleModel.objects.get_or_create(brand="Peugeot", model="308", year=2015, child_seat=True,
                                                      number_place=5,
                                                      luggage_number=50, category="Berline")

        self.vehicle = Vehicle(model=model, driver=self.driver, registration="AT-856-XR", color="Black", empty_places=5,
                               empty_luggages=50)
        self.vehicle.insurance = "/home/phayusa/Images/230045.jpg"
        self.vehicle.insurance_card = "/home/phayusa/Images/230045.jpg"
        self.vehicle.registration_card = "/home/phayusa/Images/230045.jpg"
        self.vehicle.front = "/home/phayusa/Images/230045.jpg"
        self.vehicle.back = "/home/phayusa/Images/230045.jpg"
        self.vehicle.save()

    def test_request(self):
        self.assertEqual(upload_bookings_vehicle(None).status_code, 200)

    def test_end_driver(self):
        class Request(object):
            def __init__(self, user):
                self.user = user
        request = Request(user=self.userB)
        end_driver(request)
        self.assertEqual(self.vehicle.area, None)
        # self.assertEqual(self.vehicle.driver, None)
