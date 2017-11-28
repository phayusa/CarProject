# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.shortcuts import render

from ..forms import ClientForm, DriverForm, CommercialForm, PartenerForm, UserForm


def client_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = ClientForm()
        form_user = UserForm()
    if request.user.is_superuser:
        return render(request, 'object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2, "form_user": form_user})
    else:
        return redirect('/')


def driver_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = DriverForm()
    if request.user.is_superuser:
        return render(request, 'object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2})
    else:
        return redirect('/')


def commercial_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = CommercialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = CommercialForm()
    if request.user.is_superuser:
        return render(request, 'object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2})
    else:
        return redirect('/')


def partener_create(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login')

    if request.method == "POST":
        form = PartenerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/manager/')
    else:
        form = PartenerForm()
    if request.user.is_superuser:
        return render(request, 'object_edit.html',
                      {"sections": ["Gestion", "Création"],
                       "form": form, "type": 2})
    else:
        return redirect('/')
