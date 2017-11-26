# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from Back_Source.models import Area, Client, Driver, BuissnessPartner, Commercial
from forms import ClientForm, DriverForm, CommercialForm, PartenerForm


def index(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        return render(request, 'index.html')
    else:
        return redirect('/')


def base_manager(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = ClientForm(request.POST)
        # if form.is_valid():
    else:
        form = ClientForm()

    if request.user.is_superuser:
        return render(request, 'person_manager.html', {"sections": ["Gestion Comptes"], "form": form})
    else:
        return redirect('/')


# def client_manager(request):
#     if not request.user.is_authenticated():
#         return redirect('/admin/login')
#
#     if request.method == "POST":
#         form = ClientForm(request.POST)
#         # if form.is_valid():
#     else:
#         form = ClientForm()
#
#     if request.user.is_superuser:
#         return render(request, 'clients_manager.html', {"sections": ["Clients", "Gestion"], "form": form})
#     else:
#         return redirect('/')
#
#
# def driver_manager(request):
#     if not request.user.is_authenticated():
#         return redirect('/admin/login')
#
#     if request.method == "POST":
#         form = DriverForm(request.POST)
#         # if form.is_valid():
#     else:
#         form = DriverForm()
#
#     if request.user.is_superuser:
#         return render(request, 'person_manager.html', {"sections": ["Clients", "Gestion"], "form": form})
#     else:
#         return redirect('/')


def client_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = ClientForm(request.POST, instance=Client.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = ClientForm(instance=Client.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'object_edit.html',
                      {"sections": ["Gestion", "Edition", str(pk)],
                       "form": form})
    else:
        return redirect('/')


def driver_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = DriverForm(request.POST, instance=Driver.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = DriverForm(instance=Driver.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'object_edit.html',
                      {"sections": ["Gestion", "Edition", str(pk)],
                       "form": form})
    else:
        return redirect('/')


def commercial_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = CommercialForm(request.POST, instance=Commercial.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = CommercialForm(instance=Commercial.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'object_edit.html',
                      {"sections": ["Gestion", "Edition", str(pk)],
                       "form": form})
    else:
        return redirect('/')


def partener_edit(request, pk):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = PartenerForm(request.POST, instance=BuissnessPartner.objects.get(id=pk))
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = PartenerForm(instance=BuissnessPartner.objects.get(id=pk))
    if request.user.is_superuser:
        return render(request, 'object_edit.html',
                      {"sections": ["Gestion", "Edition", str(pk)],
                       "form": form})
    else:
        return redirect('/')


def areas(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.user.is_superuser:
        if request.method == "GET":
            return render(request, 'areas.html', {"sections": ["Zones"], "areas": Area.objects.all()})
        else:
            if request.method == "POST":
                data = request.POST
                print data
                for area in Area.objects.all():
                    print area.id
                    if str(area.id) in data:
                        raw_data = data[str(area.id)].replace(",", ".").split(";")
                        if len(raw_data) == 4:
                            area.north = raw_data[0]
                            area.south = raw_data[1]
                            area.west = raw_data[2]
                            area.east = raw_data[3]
                            area.save()
                return redirect("/admin/areas/")
    else:
        return redirect('/')


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin')
                return redirect('/')
            else:
                return render(request, 'login.html')
