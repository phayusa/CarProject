# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-03 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Back_Source', '0005_travel_free_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='time_estimated',
            field=models.IntegerField(default=0, verbose_name=b'Temps estim\xc3\xa9 en seconde'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='travel',
            name='free_place',
            field=models.IntegerField(default=0, verbose_name=b'Nombre de places disponible'),
        ),
        migrations.AlterField(
            model_name='travel',
            name='start',
            field=models.DateField(blank=True, null=True, verbose_name=b'D\xc3\xa9part Pr\xc3\xa9vue'),
        ),
    ]
