from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'client/index-2.html')


def about(request):
    return render(request, 'client/about.html')


def not_found(request):
    return render(request, 'client/404.html')


def register(request):
    return render(request, 'client/login-register.html')


def prices(request):
    return render(request, 'client/prices.html')
