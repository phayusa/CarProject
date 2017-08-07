# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-07 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_place', models.IntegerField()),
                ('model', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=500)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Back_Source.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Back_Source.Person')),
                ('payment', models.CharField(max_length=5)),
            ],
            bases=('Back_Source.person',),
        ),
        migrations.AddField(
            model_name='booking',
            name='travel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Back_Source.Travel'),
        ),
        migrations.AddField(
            model_name='booking',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Back_Source.Client'),
        ),
    ]
