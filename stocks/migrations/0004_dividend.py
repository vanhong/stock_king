# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dividend',
            fields=[
                ('surrogate_key', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('date', models.DateField(db_index=True)),
                ('year', models.IntegerField(db_index=True)),
                ('symbol', models.CharField(db_index=True, max_length=20)),
                ('cash_dividends', models.DecimalField(decimal_places=3, max_digits=20, null=True)),
                ('stock_dividends_from_retained_earnings', models.DecimalField(decimal_places=3, max_digits=20, null=True)),
                ('stock_dividends_from_capital_reserve', models.DecimalField(decimal_places=3, max_digits=20, null=True)),
                ('stock_dividends', models.DecimalField(decimal_places=3, max_digits=20, null=True)),
                ('total_dividends', models.DecimalField(decimal_places=3, max_digits=20, null=True)),
                ('employee_stock_rate', models.DecimalField(decimal_places=3, max_digits=20, null=True)),
            ],
        ),
    ]
