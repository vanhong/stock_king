# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_seasonrevenue'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('surrogate_key', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('date', models.DateField(db_index=True)),
                ('user', models.CharField(max_length=20)),
                ('symbol', models.CharField(max_length=20)),
                ('rank', models.IntegerField()),
            ],
        ),
    ]
