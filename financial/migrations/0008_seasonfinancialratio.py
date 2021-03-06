# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 03:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0007_seasoncashflowstatement'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonFinancialRatio',
            fields=[
                ('surrogate_key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('symbol', models.CharField(db_index=True, max_length=20)),
                ('year', models.IntegerField(db_index=True)),
                ('season', models.IntegerField(db_index=True)),
                ('date', models.DateField(db_index=True)),
                ('gross_profit_margin', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('operating_profit_margin', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('net_profit_margin_before_tax', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('net_profit_margin', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('revenue_per_share', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('operating_profit_per_share', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('net_before_tax_profit_per_share', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('earnings_per_share', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('return_on_assets', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('return_on_equity', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('current_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('quick_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('financial_debt_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('debt_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('interest_cover', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('accounts_receivable_turnover_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('inventory_turnover_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('fixed_asset_turnover_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_asset_turnover_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('inventory_sales_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('available_for_sale_to_equity_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('intangible_asset_to_equity_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('depreciation_to_sales_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('operating_profit_to_net_profit_before_tax_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('payout_ratio', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('tax_rate', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('modified_date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['symbol', 'date'],
            },
        ),
    ]
