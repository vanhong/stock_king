# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-27 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_dividend'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateManagement',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('last_update_date', models.DateField()),
                ('last_data_date', models.DateField()),
                ('notes', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
