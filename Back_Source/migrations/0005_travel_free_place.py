# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-03 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Back_Source', '0004_auto_20180303_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='free_place',
            field=models.IntegerField(default=0),
        ),
    ]
