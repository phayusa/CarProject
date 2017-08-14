from django.shortcuts import render
from Back_Source.models import Vehicle
from django.shortcuts import render


# Create your views here.
def mapView(request):
    pois = Vehicle.objects.all()
    return render(request, 'test_map.html', {'pois': pois})
