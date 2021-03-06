# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0005_auto_20171218_0718'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonBalanceSheet',
            fields=[
                ('surrogate_key', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('symbol', models.CharField(db_index=True, max_length=20)),
                ('year', models.IntegerField(db_index=True)),
                ('season', models.IntegerField(db_index=True)),
                ('date', models.DateField(db_index=True)),
                ('total_cash_and_cash_equivalents', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_due_from_the_central_bank_and_call_loans_to_banks', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_financial_assets_at_fair_value_through_profit_or_loss', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_derivative_financial_assets_for_hedging', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_securities_purchased_under_resell_agreements', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_receivables', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_current_tax_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_assets_classified_as_held_for_sale', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_discounts_and_loans', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_available_for_sale_financial_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_held_to_maturity_financial_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_investments_measured_by_equity_method', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_restricted_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_other_financial_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_property_and_equipment', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_investment_property', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_intangible_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_deferred_tax_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_other_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_deposits_from_the_central_bank_and_banks', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_due_to_the_central_bank_and_banks', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_financial_liabilities_at_fair_value', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_notes_and_bonds_issued_under_repurchase', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_payables', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_current_tax_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_liabilities_related_to_assets_held_for_sale', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_deposits_and_remittances', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_bank_notes_payable', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_bonds_payable', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_preferred_stock_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_other_financial_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_provisions', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_deferred_income_tax_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_other_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_capital', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_capital_surplus', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_retained_earnings', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_other_equity_interest', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_treasury_shares', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_equity_attributable_to_owners_of_parent', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('equity_attributable_to_former_owner', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('equity_attributable_to_non_controlling', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('non_controlling_interests', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_equity', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('number_of_shares_in_entity_held_by_entity', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('equivalent_issue_shares_of_advance_receipts_for_common_stock', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('number_of_share_capital_awaiting_retirement', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('book_value_per_share', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_current_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_non_current_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_current_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_non_current_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_liabilities', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_reinsurance_contract_assets', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('derivative_financial_liabilities_for_hedging', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('net_commercial_papers_issued', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
                ('total_other_borrowings', models.DecimalField(decimal_places=0, max_digits=20, null=True)),
            ],
        ),
    ]
