# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-18 07:21
from __future__ import unicode_literals

from django.db import migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Back_Source', '0015_auto_20180318_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='pos',
            field=geoposition.fields.GeopositionField(blank=True, max_length=42, verbose_name=b'Position'),
        ),
    ]
