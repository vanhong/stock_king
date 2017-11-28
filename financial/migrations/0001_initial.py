# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-24 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonIncomeStatement',
            fields=[
                ('surrogate_key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('symbol', models.CharField(db_index=True, max_length=20)),
                ('year', models.IntegerField(db_index=True)),
                ('season', models.IntegerField(db_index=True)),
                ('date', models.DateField(db_index=True)),
                ('total_operating_revenue', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_operating_cost', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('gross_profit_loss_from_operations', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('unrealized_profit_loss_from_sales', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('realized_profit_loss_from_sales', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_gross_profit_from_operations', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_selling_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('administrative_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('research_and_development_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_operating_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_other_income_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_operating_income_loss', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('other_income', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('other_gains_and_losses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_finance_costs', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('share_of_profit_loss_of_associates_using_equity_method', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_non_operating_income_and_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('profit_loss_from_continuing_operations_before_tax', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_tax_expense', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('profit_loss_from_continuing_operations', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('profit_loss', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('exchange_differences_on_translation', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('unrealised_gains_losses_for_sale_financial_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_share_of_other_income_of_associates_using_equity_method', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('income_tax_related_of_other_comprehensive_income', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('other_comprehensive_income', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_other_comprehensive_income', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_comprehensive_income', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('profit_loss_attributable_to_owners_of_parent', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('profit_loss_to_non_controlling_interests', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('comprehensive_income_attributable_to_owners_of_parent', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('comprehensive_income_attributable_to_non_controlling_interests', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_basic_earnings_per_share', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_diluted_earnings_per_share', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('interest_income', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('interest_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_interest_income_expense', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_service_fee_charge_and_commisions_income_loss', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_income_loss_of_insurance_operations', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('gain_loss_on_financial_assets_liabilities_at_fair_value', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('gain_loss_on_investment_property', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('realized_gains_on_available_for_sale_financial_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('realized_gains_on_held_to_maturity_financial_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('foreign_exchange_gains_losses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('impairment_loss_or_reversal_of_impairment_loss_on_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_other_non_interest_incomes_losses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_income_loss_except_interest', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_income_loss', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_bad_debts_expense_and_guarantee_liability_provisions', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_net_change_in_provisions_for_insurance_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('employee_benefits_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('depreciation_and_amortization_expense', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('other_general_and_administrative_expenses', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('gain_loss_on_effective_portion_of_cash_flow_hedges', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('income_from_discontinued_operations', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
            ],
        ),
    ]
