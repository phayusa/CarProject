# -*- coding: utf-8 -*-

import datetime
import json
import urllib
from io import BytesIO

import pytz
import stripe
from django.conf import settings
from django.contrib.auth import login as login_func, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import *
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils.dateparse import parse_datetime
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from xhtml2pdf import pisa

from Back_Source.models import VehicleModel, Client, Booking, Airport, BuissnessPartner, Commercial, Operator, Travel, \
    Vehicle
from Localisation.views import get_area
from forms import BookingForm, ClientForm, ContactUsForm, ContactProForm
from tokens import account_activation_token


# Create your views here.


def index(request):
    # Redirect on the correct page
    if not request.user.is_authenticated():
        return render(request, 'client/index-2.html',
                      {"Airports": Airport.objects.all(), "cars": VehicleModel.objects.all()})

    if request.user.is_superuser:
        return redirect("/admin/")
    if Operator.objects.filter(user=request.user).exists():
        return redirect("/operator/")
    if BuissnessPartner.objects.filter(user=request.user).exists():
        return redirect("/partener/")
    if Commercial.objects.filter(user=request.user).exists():
        return redirect("/commercial/")

    if request.method == "GET":
        return render(request, 'client/index-2.html',
                      {"Airports": Airport.objects.all(), "cars": VehicleModel.objects.all()})
    else:
        return redirect("/404")


def about(request):
    return render(request, 'client/about.html')


def events(request):
    if request.method == "POST":
        return redirect('/')
    return render(request, 'client/events.html')


def not_found(request):
    return render(request, 'client/404.html')


def account_activation_sent(request):
    return render(request, 'mail/mail_to_confirm.html')


def register(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # is_active=False)
            # user.save()
            # client = Client(user=user, mail=user.email, first_name=data['first_name'], last_name=data['last_name'],
            #                 age=int(data['age']), gender=data['gender'], phone_number=data['phone_number'])
            client = form.save()
            user_client = client.user
            current_site = get_current_site(request)

            subject = 'Aceline Services : Confirmation du Compte'
            message = render_to_string('mail/mail_confirmation.html', {
                'user': user_client,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_client.pk)),
                'token': account_activation_token.make_token(user_client),
            })
            user_client.email_user(subject, message)
            return redirect('account_activation_sent')

            # login_func(request, client.user)
            #
            # return redirect('/')
    else:
        form = ClientForm()

    return render(request, 'client/login-register.html', {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # Update the client
        client = Client.objects.filter(user=user)[0]
        client.status = 'Actif'
        client.save()

        login_func(request, user)
        return redirect('home')
    else:
        return render(request, 'mail/mail_invalid.html')


def login(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username:
            errors['username'] = 'Champs requis'
        if not password:
            errors['password'] = 'Champs requis'
            return render(request, 'client/login-register.html', {"type": 1, "errors": errors})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login_func(request, user)
                # Force the user logout after 5 minutes of inactivity
                request.session.set_expiry(3000)
                return HttpResponseRedirect('/')
        else:
            errors['username'] = 'Nom d\'utilisateur ou Mot de passe incorrecte'
    return render(request, 'client/login-register.html', {"type": 1, "errors": errors})


def prices(request):
    models = VehicleModel.objects.all()
    return render(request, 'client/prices.html', {'models': models, "Airports": Airport.objects.all()})


def contact(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():  # Pour le moment jusqu'à j'ajoute l'envoi d'email
            return render(request, 'client/contact-us.html', {'form': form})
    else:
        form = ContactUsForm()
    return render(request, 'client/contact-us.html', {'form': form})


def contact_pro(request):
    if request.method == "POST":
        form = ContactProForm(request.POST)
        if form.is_valid():  # Pour le moment jusqu'à j'ajoute l'envoi d'email
            return render(request, 'client/contact_pro.html', {'form': form})
            #            return redirect('/')
    else:
        form = ContactProForm()
    return render(request, 'client/contact_pro.html', {'form': form})


def user(request):
    client = Client.objects.filter(user=request.user)[0]
    return render(request, 'client/user-profile.html', {"client": client})


def user_settings(request):
    client = Client.objects.filter(user=request.user)[0]
    return render(request, 'client/user-profile-settings.html', {"client": client})


def user_bookings(request):
    client = Client.objects.filter(user=request.user)[0]
    bookings = Booking.objects.filter(client=client)
    return render(request, 'client/user-profile-booking-history.html', {"client": client, "bookings": bookings})


def user_cards(request):
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = "sk_test_Tpj31pCyqiySY9503dvp2VEq"

    client = Client.objects.filter(user=request.user)[0]
    customer = get_stripe_customer(client)

    if request.method == "GET":
        # Getting stripe information
        cards = customer.sources.data
        default = customer.default_source

        return render(request, 'client/user-profile-cards.html', {"client": client, "cards": cards, "default": default})
        # TODO : add of card
        # elif request.method == "POST":


def user_bookings_delete(request, pk):
    # parsed_uri = urlparse(request.build_absolute_uri())
    # baseurl = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    # r = requests.delete(baseurl+'db/booking/'+pk, auth=(request.user.username, request.user.password))
    # print request.user.username
    # print request.user.password
    Booking.objects.filter(id=pk).delete()

    client = Client.objects.filter(user=request.user)[0]
    bookings = Booking.objects.filter(client=client)
    return render(request, 'client/user-profile-booking-history.html', {"client": client, "bookings": bookings})


def booking_succeed(request, pk):
    client = Client.objects.filter(user=request.user)[0]
    booking = Booking.objects.filter(id=pk)[0]

    message = EmailMessage('Hello', 'Body goes here', 'myprojecttest0114@gmail.com',
                           ['yahiaoui.fakhri@gmail.com'],
                           headers={'Reply-To': 'another@example.com'})
    #    attachment = open(generatePdf(), 'rb')
    message.attach("test", generate_pdf(), 'application/pdf')
    message.send()
    return render(request, 'client/success-payment.html', {"client": client, "booking": booking})


def booking_create(request, *args, **kwargs):
    if not request.user.is_authenticated():
        return redirect('/login/')
    if not request.method == "POST":
        return redirect('/404')

    data = request.POST
    date = data.get('date', None)
    #        time = data.get('time', None)

    clients = Client.objects.filter(user=request.user)
    if not clients:
        client = Client.objects.all()[0]
    else:
        client = clients[0]

    # if not time or not date:
    if not date:
        return redirect('/')
    raw_date = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")
    date_time = raw_date.strftime("%Y-%m-%dT%H:%M")

    date_w_timezone = pytz.timezone("Europe/Paris").localize(parse_datetime(date_time), is_dst=None)

    origin = str(Airport.objects.filter(id=data["airport"])[0]).replace(' ', '+').replace(',', '')
    destination = data["destination"].replace(' ', '+').replace(',', '')
    estimation_travel = compute_travel(origin, destination, date_w_timezone)

    try:
        booking = Booking.objects.create(destination=data["destination"],
                                         destination_location=data["destination_location"].replace('(',
                                                                                                   '').replace(
                                             ')',
                                             ''),
                                         airport=Airport.objects.filter(id=data["airport"])[0],
                                         # time_booking= datetimeNow.strftime("%d/%m/%Y %H:%M"),
                                         arrive_time=date_w_timezone,
                                         luggage_number=int(data['luggage_number']),
                                         passengers=int(data['passengers']),
                                         model_choose=
                                         VehicleModel.objects.filter(id=data['model_choose'])[
                                             0],
                                         client=client,
                                         flight=data["flight"],
                                         distance=float(estimation_travel['distance']['text'].replace(" km", "")),
                                         time_estimated=int(estimation_travel['duration']['value']))

        booking.save()

        request.session['Booking_id'] = booking.id
        request.session.modified = True
        return redirect('/booking/payment/')
    except Exception as e:
        raise Http404("Page non trouvé")


# Retrieve or create the customer in striped
def get_stripe_customer(client, card=None):
    if client.id_stripe:
        return stripe.Customer.retrieve(client.id_stripe)
    # create the customer with the given credit card
    if card:
        customer = stripe.Customer.create(email=client.mail,
                                          description="Customer for " + str(client.id) + " client",
                                          source=card)
    else:
        customer = stripe.Customer.create(email=client.mail,
                                          description="Customer for " + str(client.id) + " client")
    # Save it in the client data
    client.id_stripe = customer.id
    client.save()

    # Return the getting customer
    return customer


def booking_payment(request):
    # try:
    booking_pending_id = request.session.get('Booking_id', False)
    if not booking_pending_id:
        raise Http404("Page non trouvé")

    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = "sk_test_Tpj31pCyqiySY9503dvp2VEq"

    client = Client.objects.filter(user=request.user).first()
    customer = None

    if request.user.is_authenticated:
        customer = get_stripe_customer(client)
    booking_pending = Booking.objects.filter(id=booking_pending_id).first()

    if request.method == "GET":

        if customer:
            # Getting stripe information
            cards = customer.sources.data
            default = customer.default_source

            return render(request, 'client/payment.html',
                          {"booking": booking_pending, "cards": cards, "default": default})

        return render(request, 'client/payment.html', {"booking": booking_pending})
    elif request.method == "POST":

        # Token is created using Checkout or Elements!
        # Get the payment token ID submitted by the form:
        token = request.POST['stripeToken']  # Using Flask

        if customer:

            card = customer.sources.retrieve(token)
            if not card:
                # Add the new card to the stripe customer
                customer.sources.create(source=token)
                customer.save()

            # Charge the user's card:
            charge = stripe.Charge.create(
                amount=500,
                currency="eur",
                description="Reservation Aceline Services",
                # Charge the card
                # source=customer.default_source,
                source=card,
                # Charge the customer
                customer=customer.id
            )
        else:
            # Charge the user's card:
            charge = stripe.Charge.create(
                amount=500,
                currency="eur",
                description="Reservation Aceline Services",
                # Charge the card
                source=token
            )

        booking_pending.status = "Validé"
        booking_pending.save()

        create_travel(booking_pending)

        request.session['Booking_id'] = None
        return redirect('/booking/succeed/' + str(booking_pending_id))
    else:
        raise Http404("Page non trouvé")


def create_travel(booking_to_test):
    area = get_area(booking_to_test)
    place_wanted = booking_to_test.passengers
    estimated_arrive = booking_to_test.arrive_time + datetime.timedelta(seconds=booking_to_test.time_estimated) * 2

    if place_wanted == 0:
        travels = None
    else:
        travels = Travel.objects.filter(start=booking_to_test.arrive_time,
                                        free_place__gte=place_wanted,
                                        area=area, airport=booking_to_test.airport)

    # The case with no travel found
    if not travels:
        travel = Travel.objects.create(start=booking_to_test.arrive_time,
                                       free_place=booking_to_test.model_choose.number_place - place_wanted,
                                       area=area, airport=booking_to_test.airport,
                                       car=free_car(area, booking_to_test.arrive_time, estimated_arrive),
                                       end=estimated_arrive)
    else:
        travel = travels[0]

        travel.free_place -= place_wanted

    travel.bookings.add(booking_to_test)

    if travel.bookings.count() > 1:
        # Optimise travel with multiples destination
        compute_travel_multiples(booking_to_test.airport, booking_to_test.arrive_time, travel)

    # update the travel
    travel.save()


def free_car(area, date_start, date_end):
    car_test = None

    cars = Vehicle.objects.all()
    for car_test in cars:
        # We find if we found that the car is busy during this period of time
        travels = Travel.objects.filter(start__lte=date_start, end__gte=date_start, car=car_test)
        if travels:
            continue

        # Testing if we have something between the travel
        travels = Travel.objects.filter(start__gte=date_start, end__lte=date_end, car=car_test)
        if travels:
            continue

        # Testing if this car have not others area assigned this day
        travels = Travel.objects.filter(start__day=date_start.day, car=car_test).exclude(area=area).exclude(area=None)
        if travels:
            continue

        # If we pass all the test we got the good car
        return car_test
    return car_test


def retrieve_customer_charge(customer):
    return stripe.Charge.list(customer=customer.id)


def booking(request, *args, **kwargs):
    # print request.GET.get('start','n,nbn')
    tmp = {}
    model = request.GET.get('model', None)
    if model:
        tmp["model_choose"] = model
    date = request.GET.get('date', None)
    time = request.GET.get('time', None)

    if time and date:
        raw_date = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %I:%M %p")
        # tmp["arrive_time"] = raw_date.strftime("%d/%m/%Y %H:%M")
        tmp["arrive_time"] = raw_date.strftime("%Y-%m-%dT%H:%M")

    user_client = Client.objects.filter(user=request.user)
    print user_client
    if user_client:
        tmp["client"] = user_client[0].id

    arrive = request.GET.get('arrive', None)
    airport = request.GET.get('airport', None)
    passengers = request.GET.get('passengers', None)

    if arrive:
        tmp["destination"] = arrive

    if airport:
        tmp["airport"] = airport

    if passengers:
        tmp["passengers"] = passengers

    form = BookingForm(tmp)
    return render(request, 'client/booking.html', {'form': form})


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()  # HttpResponse(result.getValue(), content_type='application/pdf')
    return None


def generate_pdf():
    template = get_template('pdf/invoice.html')
    context = {
        "Date d'achat": "Today",
        "Nom": 123,
        "Prénom": "John Cooper",
        "Adresse": 1399.99,
        "Email": "Today",
        "Modèle de voiture": "Today",
        "N° vol": "Today",
        "Prix": "Today",
    }

    html = template.render(context)
    pdf = render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % "12341231"
        content = "inline; filename='%s'" % filename
        content = "attachment; filename='%s'" % filename
        response['Content-Disposition'] = content
    # return response
    return pdf  # HttpResponse("Not Found")


def compute_travel(origin, destination, departure_time):
    raw_url_api = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + str(origin) + '&destination=' + str(
        destination) + '&units=metric&key=' + str(
        settings.GEOPOSITION_GOOGLE_MAPS_API_KEY) + '&departure_time=' + str(int(
        (departure_time - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()))

    print raw_url_api
    result = json.load(urllib.urlopen(raw_url_api))

    return result['routes'][0]['legs'][0]


def compute_travel_multiples(origin, departure_time, travel):
    raw_url_api = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + str(origin) + '&destination=' + str(
        origin) + '&units=metric&key=' + str(
        settings.GEOPOSITION_GOOGLE_MAPS_API_KEY) + '&departure_time=' + str(int(
        (departure_time - datetime.datetime(1970, 1, 1,
                                            tzinfo=pytz.utc)).total_seconds())) + '&waypoints=optimize:true|'
    stock = []
    second_estimated = 0
    places = 0
    model = 0
    for booking_test in travel.bookings.all():
        raw_url_api += str(booking_test.destination) + '|'
        stock.append(booking_test)
        places += booking_test.passengers
        if model == 0:
            model = booking_test.model_choose.number_place

    print raw_url_api
    result = json.load(urllib.urlopen(raw_url_api))['routes'][0]
    travel.bookings.clear()

    # sort travel with optimun way
    for order in result['waypoint_order']:
        travel.bookings.add(stock[order])
        second_estimated += result['legs'][order]['duration']['value']

    # update the estimated time
    travel.end = travel.start + datetime.timedelta(seconds=second_estimated)

    # update the number of place
    travel.free_place = model - places
