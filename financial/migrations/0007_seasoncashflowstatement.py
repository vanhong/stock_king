# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-28 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0006_seasonbalancesheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonCashflowStatement',
            fields=[
                ('surrogate_key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('symbol', models.CharField(db_index=True, max_length=20)),
                ('year', models.IntegerField(db_index=True)),
                ('season', models.IntegerField(db_index=True)),
                ('date', models.DateField(db_index=True)),
                ('profit_loss_from_continuing_operations_before_tax', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('profit_loss_before_tax', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('depreciation_expense', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('amortization_expense', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('interest_expense', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('interest_income', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('share_based_payments', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('share_of_profit_loss_of_associates_using_equity_method', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('loss_gain_on_disposal_of_property_plan_and_equipment', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('loss_gain_on_disposal_of_investments', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('loss_gain_on_disposal_of_investments_using_equity_method', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('impairment_loss_on_financial_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('impairment_loss_on_non_financial_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('realized_loss_profit_on_from_sales', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('unrealized_foreign_exchange_loss_gain', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('other_adjustments_to_reconcile_profit_loss', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('total_adjustments_to_reconcile_profit_loss', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_increase_in_financial_assets_held_for_trading', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_increase_in_derivative_financial_assets_for_hedging', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_increase_in_accounts_receivable', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_increase_in_accounts_receivable_from_related_parties', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_increase_in_other_receivable_due_from_related_parties', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_increase_in_inventories', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_increase_in_other_current_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_increase_in_other_financial_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('total_changes_in_operating_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_decrease_in_accounts_payable', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_decrease_in_accounts_payable_to_related_parties', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_decrease_in_provisions', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_decrease_in_other_current_liabilities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_decrease_in_accrued_pension_liabilities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_decrease_in_other_operating_liabilities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('total_changes_in_operating_liabilities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('total_changes_in_operating_assets_and_liabilities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('total_adjustments', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('cash_inflow_outflow_generated_from_operations', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('income_taxes_refund_paid', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('net_cash_flows_from_used_in_operating_activities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('acquisition_of_available_for_sale_financial_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('proceeds_from_disposal_of_available_for_sale_financial_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('acquisition_of_held_to_maturity_financial_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('proceeds_from_repayments_of_held_to_maturity_financial_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('acquisition_of_financial_assets_at_cost', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('proceeds_from_disposal_of_financial_assets_at_cost', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('proceeds_from_disposal_of_investments_using_equity_method', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('proceeds_from_disposal_of_subsidiaries', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('acquisition_of_property_plant_and_equipment', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('proceeds_from_disposal_of_property_plant_and_equipment', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_in_refundable_deposits', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_in_refundable_deposits', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('acquisition_of_intangible_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_in_long_term_lease_and_installment_receivables', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_in_other_financial_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_in_other_non_current_assets', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('interest_received', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('dividends_received', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('other_investing_activities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('net_cash_flows_from_used_in_investing_activities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_in_short_term_loans', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('proceeds_from_issuing_bonds', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('repayments_of_bonds', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('proceeds_from_long_term_debt', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('repayments_of_long_term_debt', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('increase_in_guarantee_deposits_received', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_in_guarantee_deposits_received', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('decrease_in_lease_payable', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('exercise_of_employee_share_options', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('interest_paid', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('change_in_non_controlling_interests', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('other_financing_activities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('net_cash_flows_from_used_in_financing_activities', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('effect_of_exchange_rate_changes_on_cash_and_cash_equivalents', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('net_increase_decrease_in_cash_and_cash_equivalents', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('cash_and_cash_equivalents_at_beginning_of_period', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('cash_and_cash_equivalents_at_end_of_period', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('cash_and_cash_equivalents_in_the_statement_of_financial_position', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
                ('free_cash_flow', models.DecimalField(decimal_places=0, default=0, max_digits=20)),
            ],
        ),
    ]
