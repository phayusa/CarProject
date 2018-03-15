# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-03 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Back_Source', '0010_auto_20180304_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='free_luggage',
            field=models.IntegerField(default=0, verbose_name=b'Nombre de baggages disponibles'),
        ),
        migrations.AlterField(
            model_name='vehiclemodel',
            name='price',
            field=models.FloatField(default=0, verbose_name=b'Prix au km'),
        ),
    ]
