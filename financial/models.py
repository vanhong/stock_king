# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
# 綜合損益表(季)
class SeasonIncomeStatement(models.Model):
	surrogate_key = models.CharField(max_length=50, primary_key=True)
	symbol = models.CharField(max_length=20, db_index=True)
	year = models.IntegerField(db_index=True)
	season = models.IntegerField(db_index=True)
	date = models.DateField(db_index=True)
	data_date = models.DateField(db_index=True)
	# 營業收入合計
	total_operating_revenue = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業成本合計
	total_operating_cost = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業毛利(毛損)
	gross_profit_loss_from_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 未實現銷貨損益
	unrealized_profit_loss_from_sales = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 已實現銷貨損益
	realized_profit_loss_from_sales = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業毛利(毛損)淨額
	net_gross_profit_from_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 推銷費用
	total_selling_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 管理費用
	administrative_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 研究發展費用
	research_and_development_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業費用合計
	total_operating_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他收益及費損淨額
	net_other_income_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業利益
	net_operating_income_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其它收入
	other_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其它利益及損失金額
	other_gains_and_losses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 財務成本淨額
	net_finance_costs = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 採用權益法認列之關聯企業及合資損益之份額淨額
	# Share of profit (loss) of associates and joint ventures accounted for using equity method, net
	share_of_profit_loss_of_associates_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業外收入及支出合計
	total_non_operating_income_and_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 稅前淨利(淨損)
	profit_loss_from_continuing_operations_before_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 所得稅費用(利益合計)
	total_tax_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 繼續營業單位本期淨利(淨損)
	profit_loss_from_continuing_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 本期淨利
	profit_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 國外營運機構財務報表換算之兌換差額
	exchange_differences_on_translation = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 備供出售金融資產未實現評價損益
	unrealised_gains_losses_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 採用權益法認列之關聯企業及合資之其他綜合損益之份額合計
	# Total share of other comprehensive income of associates and joint ventures accounted for using equity method 
	total_share_of_other_income_of_associates_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 與其他綜合損益組成部分相關之所得稅
	income_tax_related_of_other_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他綜合損益
	other_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他綜合損益（淨額）
	net_other_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 本期綜合損益總額
	total_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 母公司業主（淨利／損）
	profit_loss_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 非控制權益（淨利／損）
	profit_loss_to_non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 母公司業主（綜合損益）
	comprehensive_income_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 非控制權益（綜合損益）
	comprehensive_income_attributable_to_non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 基本每股盈餘
	total_basic_earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 稀釋每股盈餘
	total_diluted_earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# !!!!!!!!!!!!!!!金融股!!!!!!!!!!!!!!!!!!!!!!
	# 利息收入
	interest_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 減：利息費用
	interest_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 利息淨收益
	net_interest_income_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 手續費及佣金淨收益
	net_service_fee_charge_and_commisions_income_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 保險業務淨收益
	net_income_loss_of_insurance_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 透過損益按公允價值衡量之金融資產及負債損益
	gain_loss_on_financial_assets_liabilities_at_fair_value = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 投資性不動產損益
	gain_loss_on_investment_property = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 備供出售金融資產之已實現損益
	realized_gains_on_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持有至到期日金融資產之已實現損益
	realized_gains_on_held_to_maturity_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 兌換損益
	foreign_exchange_gains_losses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資產減損（損失）迴轉利益淨額
	impairment_loss_or_reversal_of_impairment_loss_on_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他利息以外淨損益
	net_other_non_interest_incomes_losses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 利息以外淨損益
	net_income_loss_except_interest = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 淨收益
	net_income_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 呆帳費用及保證責任準備提存（各項提存）
	total_bad_debts_expense_and_guarantee_liability_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 保險負債準備淨變動
	total_net_change_in_provisions_for_insurance_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 員工福利費用
	employee_benefits_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 折舊及攤銷費用
	depreciation_and_amortization_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他業務及管理費用
	other_general_and_administrative_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 現金流量避險中屬有效避險不分之避險工具利益(損失)
	gain_loss_on_effective_portion_of_cash_flow_hedges = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 停業單位損益
	income_from_discontinued_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	#-----------end--------------#	
	def percent_operating_revenue(self):
		return total_operating_revenue / total_operating_revenue
	def percent_operating_cost(self):
		return operating_cost / total_operating_revenue
	def percent_gross_profit_from_operations(self):
		return gross_profit_from_operations / total_operating_revenue
	def percent_selling_expenses(self):
		return selling_expenses / total_operating_revenue
	def percent_administrative_expenses(self):
		return administrative_expenses / total_operating_revenue
	def percent_research_and_development_expenses(self):
		return research_and_development_expenses / total_operating_revenue
	def percent_operating_expenses(self):
		return operating_expenses / total_operating_revenue
	def percent_net_operating_income(self):
		return net_operating_income / total_operating_revenue
	def percent_other_income(self):
		return other_income / total_operating_revenue
	def percent_other_gains_and_losses(self):
		return other_gains_and_losses / total_operating_revenue
	def percent_finance_costs(self):
		return finance_costs / total_operating_revenue
	def percent_non_operating_income_and_expenses(self):
		return non_operating_income_and_expenses / total_operating_revenue
	def percent_profit_from_continuing_operations_before_tax(self):
		return profit_from_continuing_operations_before_tax / total_operating_revenue
	def percent_tax_expense(self):
		return tax_expense / total_operating_revenue
	def percent_profit_from_continuing_operations(self):
		return profit_from_continuing_operations / total_operating_revenue
	def percent_profit(self):
		return profit / total_operating_revenue
	def percent_exchange_differences_on_translation(self):
		return exchange_differences_on_translation / total_operating_revenue
	def percent_unrealised_gains_for_sale_financial_assets(self):
		return unrealised_gains_for_sale_financial_assets / total_operating_revenue
	def percent_income_tax_of_other_comprehensive_income(self):
		return other_comprehensive_income / total_operating_revenue
	def percent_total_comprehensive_income(self):
		return total_comprehensive_income / total_operating_revenue
	def percent_profit_to_owners_of_parent(self):
		return profit_to_owners_of_parent / total_operating_revenue
	def percent_profit_to_non_controlling_interests(self):
		return profit_to_non_controlling_interests / total_operating_revenue
	def percent_comprehensive_income_to_owners_of_parent(self):
		return comprehensive_income_to_owners_of_parent / total_operating_revenue
	def percent_comprehensive_income_to_non_controlling_interests(self):
		return comprehensive_income_to_non_controlling_interests / total_operating_revenue
# 資產負債表(季)
class SeasonBalanceSheet(models.Model):
	surrogate_key = models.CharField(max_length=20, primary_key=True)
	year = models.IntegerField(db_index=True)
	season = models.IntegerField(db_index=True)
	symbol = models.CharField(max_length=20, db_index=True)
	date = models.DateField(db_index=True)
	data_date = models.DateField(db_index=True)
	# 現金與流動現金
	total_cash_and_cash_equivalents = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 無活絡市場之債券投資－流動淨額
	current_bond_investment_without_active_market = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 透過損益按公允價值衡量之金融資產－流動
	current_financial_assets_at_fair_value_through_profit_or_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 備供出售金融資產－流動淨額
	current_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持有至到期日金融資產－流動淨額
	current_held_to_maturity_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應收票據淨額
	notes_receivable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應收票據－關係人淨額
	notes_receivable_due_from_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應收帳款淨額
	accounts_receivable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應收帳款－關係人淨額
	accounts_receivable_due_from_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他應收款淨額
	net_other_receivables = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他應收款－關係人淨額
	other_receivables_due_from_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 當期所得稅資產
	total_current_tax_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 存貨
	total_inventories = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 生物資產流動淨額
	current_biological_asset = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 預付款項
	total_prepayments = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他流動資產
	total_other_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 流動資產合計
	total_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 備供出售金融資產－非流動淨額
	non_current_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持有至到期日金融資產－非流動淨額
	non_current_held_to_maturity_financial_assets_net = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 避險之衍生金融資產－非流動
	derivative_non_current_financial_assets_for_hedging = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 以成本衡量之金融資產－非流動淨額
	non_current_financial_assets_at_cost = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 採用權益法之投資淨額
	investment_accounted_for_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 不動產、廠房及設備
	total_property_plant_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 投資性不動產淨額
	net_investment_property = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 無形資產
	intangible_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 遞延所得稅資產
	deferred_tax_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他非流動資產
	total_other_non_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 非流動資產合計
	total_non_current_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資產總額
	total_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	
	# 短期借款
	total_short_term_borrowings = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應付短期票券
	short_term_notes_and_bills_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 透過損益按公允價值衡量之金融負債－流動
	current_financial_liabilities_fair_value = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 透過損益按公允價值衡量之金融負債－非流動
	non_current_financial_liabilities_fair_value = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 避險之衍生金融負債－流動
	current_derivative_financial_liabilities_for_hedging = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應付票據
	total_notes_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應付帳款
	total_accounts_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應付帳款－關係人
	total_accounts_payable_to_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應付建造合約款
	construction_contracts_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應付建造合約款－關係人
	construction_contracts_payable_to_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他應付款
	total_other_payables = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他應付款－關係人
	other_payables_to_related_parties = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 當期所得稅負債
	current_tax_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 負債準備－流動
	current_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他流動負債
	total_other_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 流動負債合計
	total_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 避險之衍生金融負債－非流動
	non_current_derivative_financial_liabilities_for_hedeging = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應付公司債
	total_bonds_payable = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 長期借款
	total_long_term_borrowings = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 負債準備－非流動
	total_non_current_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 遞延所得稅負債
	total_deferred_tax_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他非流動負債
	other_non_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 非流動負債合計
	total_non_current_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 負債總額
	total_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)

	# 普通股股本
	ordinary_share = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 預收股本
	advance_receipts_for_share_capital = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 股本合計 or 股本
	total_capital_stock = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資本公積－發行溢價
	additional_paid_in_capital = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資本公積－取得或處分子公司股權價格與帳面價值差額
	capital_surplus_difference_between_consideration = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資本公積－受贈資產
	total_capital_surplus_donated_assets_received = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資本公積－採用權益法認列關聯企業及合資股權淨值之變動數
	capital_surplus_changes_in_equity_of_associates = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資本公積－庫藏股票交易
	treasury_share_transactions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資本公積－合併溢額
	net_assets_from_merger = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資本公積－其他
	other_capital_surplus = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 基本公積合計 or 基本公積
	total_capital_surplus = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 法定盈餘公積
	legal_reserve = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 特別盈餘公積
	special_reserve = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 未分配盈餘（或待彌補虧損）
	total_unappropriated_retained_earnings_or_accumulated_deficit = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 保留盈餘合計 or 保留盈餘
	total_retained_earnings = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他權益合計
	total_other_equity_interest = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 國外營運機構財務報表換算之兌換差額
	exchange_differences_of_foreign_financial_statements = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 備供出售金融資產未實現損益
	unrealised_gains_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 庫藏股票
	treasury_share = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 歸屬於母公司業主之權益合計 or 
	total_equity_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 共同控制下前手權益
	equity_attributable_to_former_owner_of_business_combination = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 非控制權益
	non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 權益總額
	total_equity = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 待註銷股本股數（單位：股）
	number_of_shares_capital_awaiting_retirement = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 預收股款（權益項下）之約當發行股數（單位：股）
	equivalent_issue_shares_of_advance_receipts = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 母公司暨子公司所持有之母公司庫藏股股數（單位：股）
	number_of_shares_in_entity_held_by_entity = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# !!!!!!!!!金融股
	# 存放央行及拆款同業
	due_from_the_central_bank_and_call_loans_to_banks = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 避險之衍生金融資產
	derivative_financial_assets_for_hedging = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 待出售資產－淨額
	net_assets_classified_as_held_for_sale = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 貼現及放款－淨額
	net_loans_discounted = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 再保險合約資產－淨額
	net_reinsurance_contract_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他金融資產－淨額
	net_other_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 不動產及設備－淨額
	net_property_and_equipment = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他資產－淨額
	net_other_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 央行及金融同業存款
	deposits_from_the_central_bank_and_banks = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 央行及同業融資
	due_to_the_central_bank_and_banks = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 附買回票券及債券負債
	securities_sold_under_repurchase_agreements = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 應付商業本票－淨額
	net_commercial_papers_issued = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 存款及匯款
	deposits = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 負債準備
	total_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他金融負債
	total_other_financial_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他負債
	total_other_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
# 現金流量表(季)
class SeasonCashflowStatement(models.Model):
	surrogate_key = models.CharField(max_length=50, primary_key=True)
	symbol = models.CharField(max_length=20, db_index=True)
	year = models.IntegerField(db_index=True)
	season = models.IntegerField(db_index=True)
	date = models.DateField(db_index=True)
	data_date = models.DateField(db_index=True)
	#---營業活動之現金流量-間接法---
	# 繼續營業單位稅前淨利（淨損）
	profit_loss_from_continuing_operations_before_tax = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 本期稅前淨利（淨損）
	profit_loss_before_tax = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 折舊費用
	depreciation_expense = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 攤銷費用
	amortization_expense = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 利息費用
	interest_expense = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 利息收入
	interest_income = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 股份基礎給付酬勞成本
	share_based_payments = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 採用權益法認列之關聯企業及合資損失（利益）之份額
	share_of_profit_loss_of_associates_using_equity_method = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分及報廢不動產、廠房及設備損失（利益）
	loss_gain_on_disposal_of_property_plan_and_equipment = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分投資損失（利益）
	loss_gain_on_disposal_of_investments = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分採用權益法之投資損失（利益）
	loss_gain_on_disposal_of_investments_using_equity_method = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 金融資產減損損失
	impairment_loss_on_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 非金融資產減損損失
	impairment_loss_on_non_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 已實現銷貨損失（利益）
	realized_loss_profit_on_from_sales = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 未實現外幣兌換損失（利益）
	unrealized_foreign_exchange_loss_gain = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他項目
	other_adjustments_to_reconcile_profit_loss = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 不影響現金流量之收益費損項目合計
	total_adjustments_to_reconcile_profit_loss = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 持有供交易之金融資產（增加）減少
	decrease_increase_in_financial_assets_held_for_trading = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 避險之衍生金融資產（增加）減少
	decrease_increase_in_derivative_financial_assets_for_hedging = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應收帳款（增加）減少
	decrease_increase_in_accounts_receivable = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應收帳款－關係人（增加）減少
	decrease_increase_in_accounts_receivable_from_related_parties = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他應收款－關係人（增加）減少
	decrease_increase_in_other_receivable_due_from_related_parties = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存貨（增加）減少
	decrease_increase_in_inventories = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他流動資產（增加）減少
	decrease_increase_in_other_current_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他金融資產（增加）減少
	decrease_increase_in_other_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 與營業活動相關之資產之淨變動合計
	total_changes_in_operating_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應付帳款（增加）減少
	increase_decrease_in_accounts_payable = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應付帳款－關係人（增加）減少
	increase_decrease_in_accounts_payable_to_related_parties = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 負債準備增加（減少）
	increase_decrease_in_provisions = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他流動負債增加（減少）
	increase_decrease_in_other_current_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應計退休金負債增加（減少）
	increase_decrease_in_accrued_pension_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他營業負債增加（減少）
	increase_decrease_in_other_operating_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 與營業活動相關之負債之淨變動合計
	total_changes_in_operating_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 與營業活動相關之資產及負債之淨變動合計
	total_changes_in_operating_assets_and_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 調整項目合計
	total_adjustments = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 營運產生之現金流入（流出）
	cash_inflow_outflow_generated_from_operations = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 退還（支付）之所得稅
	income_taxes_refund_paid = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 營業活動之淨現金流入（流出）
	net_cash_flows_from_used_in_operating_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# ---投資活動之現金流量---
	# 取得備供出售金融資產
	acquisition_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分備供出售金融資產
	proceeds_from_disposal_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 取得持有至到期日金融資產
	acquisition_of_held_to_maturity_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 持有至到期日金融資產到期還本
	proceeds_from_repayments_of_held_to_maturity_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 取得以成本衡量之金融資產
	acquisition_of_financial_assets_at_cost = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分以成本衡量之金融資產
	proceeds_from_disposal_of_financial_assets_at_cost = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分採用權益法之投資
	proceeds_from_disposal_of_investments_using_equity_method = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分子公司
	proceeds_from_disposal_of_subsidiaries = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 取得不動產、廠房及設備
	acquisition_of_property_plant_and_equipment = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分不動產、廠房及設備
	proceeds_from_disposal_of_property_plant_and_equipment = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存出保證金增加
	increase_in_refundable_deposits = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存出保證金減少
	decrease_in_refundable_deposits = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 取得無形資產
	acquisition_of_intangible_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 長期應收租賃款減少 or 應收租賃款減少
	decrease_in_long_term_lease_and_installment_receivables = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他金融資產增加
	increase_in_other_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他非流動資產增加
	increase_in_other_non_current_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 收取之利息
	interest_received = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 收取之股利
	dividends_received = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他投資活動
	other_investing_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 投資活動之淨現金流入（流出）
	net_cash_flows_from_used_in_investing_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# ---籌資活動之現金流量---
	# 短期借款增加
	increase_in_short_term_loans = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 發行公司債
	proceeds_from_issuing_bonds = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 償還公司債
	repayments_of_bonds = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 舉借長期借款
	proceeds_from_long_term_debt = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 償還長期借款
	repayments_of_long_term_debt = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存入保證金增加
	increase_in_guarantee_deposits_received = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存入保證金減少
	decrease_in_guarantee_deposits_received = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應付租賃款減少
	decrease_in_lease_payable = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 員工執行認股權
	exercise_of_employee_share_options = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 支付之利息
	interest_paid = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 非控制權益變動
	change_in_non_controlling_interests = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他籌資活動
	other_financing_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 籌資活動之淨現金流入（流出）
	net_cash_flows_from_used_in_financing_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 匯率變動對現金及約當現金之影響
	effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 本期現金及約當現金增加（減少）數
	net_increase_decrease_in_cash_and_cash_equivalents = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 期初現金及約當現金餘額
	cash_and_cash_equivalents_at_beginning_of_period = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 期末現金及約當現金餘額
	cash_and_cash_equivalents_at_end_of_period = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 資產負債表帳列之現金及約當現金
	cash_and_cash_equivalents_in_the_statement_of_financial_position = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 自由現金流量
	free_cash_flow = models.DecimalField(max_digits=20, decimal_places=0, default=0)
# 財務比率表(季)
class SeasonFinancialRatio(models.Model):
	surrogate_key = models.CharField(max_length=50, primary_key=True)
	symbol = models.CharField(max_length=20, db_index=True)
	year = models.IntegerField(db_index=True)
	season = models.IntegerField(db_index=True)
	date = models.DateField(db_index=True)
	data_date = models.DateField(db_index=True)
	# ---獲利能力---
	# 營業毛利率 = 營業毛利 / 營業收入
	gross_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 營業利益率 = 營業利益 / 營業收入
	operating_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 稅前淨利率 = 稅前純益 / 營業收入
	net_profit_margin_before_tax = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 稅後淨利率 = 稅後純益 / 營業收入
	net_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 每股營業額(元)
	revenue_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
	# 每股營業利益(元)
	operating_profit_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
	# 每股稅前淨利(元)
	net_before_tax_profit_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
	# 每股盈餘(EPS)
	earnings_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
	# 總資產報酬率(ROA)
	return_on_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 股東權益報酬率(ROE) = 本期淨利(稅前) / 期初期末平均之權益總額(期初股東權益+期末股東權益/2)
	return_on_equity = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# ---償債能力---
	# 流動比率
	current_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 速動比率
	quick_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 金融負債比率
	financial_debt_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 負債比率
	debt_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 利息保障倍數
	interest_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	# ---經營能力---
	# 應收帳款週轉率
	accounts_receivable_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 存貨週轉率
	inventory_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 固定資產週轉率
	fixed_asset_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 總資產週轉率
	total_asset_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# ---黃國華指標---
	# 存貨營收比
	inventory_sales_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 備供出售比率
	available_for_sale_to_equity_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 無形資產比率
	intangible_asset_to_equity_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 折舊負擔比率
	depreciation_to_sales_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 營業利益佔稅前淨利比率
	operating_profit_to_net_profit_before_tax_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 現金股息配發率
	payout_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 營業稅率
	tax_rate = models.DecimalField(max_digits=20, decimal_places=2, null=True)

	modified_date = models.DateField(auto_now=True)

	#def __unicode__(self):
	#	return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.surrogate_key, self.symbol, self.date, 
	#		self.gross_profit_margin, self.operating_profit_margin, self.net_profit_margin,
	#		self.earnings_per_share, self.return_on_assets, self.return_on_equity,
	#		self.current_ratio, self.quick_ratio, self.financial_debt_ratio, self.debt_ratio,
	#		self.accounts_receivable_turnover_ratio, self.inventory_turnover_ratio,
	#		self.fixed_asset_turnover_ratio, self.total_asset_turnover_ratio,
	#		self.inventory_sales_ratio,self.available_for_sale_to_equity_ratio,
	#		self.intangible_asset_to_equity_ratio,self.undepreciation_ratio,
	#		self.depreciation_to_sales_ratio,self.operating_profit_to_net_profit_before_tax_ratio,
	#		self.payout_ratio , self.tax_rate ,self.modified_date)
	class Meta:
		ordering = ['symbol', 'date']
	class Admin:
		pass
# 綜合損益表(年)
class YearIncomeStatement(models.Model):
	surrogate_key = models.CharField(max_length=50, primary_key=True)
	symbol = models.CharField(max_length=20, db_index=True)
	year = models.IntegerField(db_index=True)
	date = models.DateField(db_index=True)
	data_date = models.DateField(db_index=True)
	# 營業收入合計
	total_operating_revenue = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業成本合計
	total_operating_cost = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業毛利(毛損)
	gross_profit_loss_from_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 未實現銷貨損益
	unrealized_profit_loss_from_sales = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 已實現銷貨損益
	realized_profit_loss_from_sales = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業毛利(毛損)淨額
	net_gross_profit_from_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 推銷費用
	total_selling_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 管理費用
	administrative_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 研究發展費用
	research_and_development_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業費用合計
	total_operating_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他收益及費損淨額
	net_other_income_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業利益
	net_operating_income_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其它收入
	other_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其它利益及損失金額
	other_gains_and_losses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 財務成本淨額
	net_finance_costs = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 採用權益法認列之關聯企業及合資損益之份額淨額
	# Share of profit (loss) of associates and joint ventures accounted for using equity method, net
	share_of_profit_loss_of_associates_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 營業外收入及支出合計
	total_non_operating_income_and_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 稅前淨利(淨損)
	profit_loss_from_continuing_operations_before_tax = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 所得稅費用(利益合計)
	total_tax_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 繼續營業單位本期淨利(淨損)
	profit_loss_from_continuing_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 本期淨利
	profit_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 國外營運機構財務報表換算之兌換差額
	exchange_differences_on_translation = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 備供出售金融資產未實現評價損益
	unrealised_gains_losses_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 採用權益法認列之關聯企業及合資之其他綜合損益之份額合計
	# Total share of other comprehensive income of associates and joint ventures accounted for using equity method 
	total_share_of_other_income_of_associates_using_equity_method = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 與其他綜合損益組成部分相關之所得稅
	income_tax_related_of_other_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他綜合損益
	other_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他綜合損益（淨額）
	net_other_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 本期綜合損益總額
	total_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 母公司業主（淨利／損）
	profit_loss_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 非控制權益（淨利／損）
	profit_loss_to_non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 母公司業主（綜合損益）
	comprehensive_income_attributable_to_owners_of_parent = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 非控制權益（綜合損益）
	comprehensive_income_attributable_to_non_controlling_interests = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 基本每股盈餘
	total_basic_earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 稀釋每股盈餘
	total_diluted_earnings_per_share = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# !!!!!!!!!!!!!!!金融股!!!!!!!!!!!!!!!!!!!!!!
	# 利息收入
	interest_income = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 減：利息費用
	interest_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 利息淨收益
	net_interest_income_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 手續費及佣金淨收益
	net_service_fee_charge_and_commisions_income_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 保險業務淨收益
	net_income_loss_of_insurance_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 透過損益按公允價值衡量之金融資產及負債損益
	gain_loss_on_financial_assets_liabilities_at_fair_value = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 投資性不動產損益
	gain_loss_on_investment_property = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 備供出售金融資產之已實現損益
	realized_gains_on_available_for_sale_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 持有至到期日金融資產之已實現損益
	realized_gains_on_held_to_maturity_financial_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 兌換損益
	foreign_exchange_gains_losses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 資產減損（損失）迴轉利益淨額
	impairment_loss_or_reversal_of_impairment_loss_on_assets = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他利息以外淨損益
	net_other_non_interest_incomes_losses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 利息以外淨損益
	net_income_loss_except_interest = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 淨收益
	net_income_loss = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 呆帳費用及保證責任準備提存（各項提存）
	total_bad_debts_expense_and_guarantee_liability_provisions = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 保險負債準備淨變動
	total_net_change_in_provisions_for_insurance_liabilities = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 員工福利費用
	employee_benefits_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 折舊及攤銷費用
	depreciation_and_amortization_expense = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 其他業務及管理費用
	other_general_and_administrative_expenses = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 現金流量避險中屬有效避險不分之避險工具利益(損失)
	gain_loss_on_effective_portion_of_cash_flow_hedges = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	# 停業單位損益
	income_from_discontinued_operations = models.DecimalField(max_digits=20, decimal_places=0, null=True)
	#-----------end--------------#
# 現金流量表(年)
class YearCashflowStatement(models.Model):
	surrogate_key = models.CharField(max_length=20, primary_key=True)
	year = models.IntegerField(db_index=True)
	symbol = models.CharField(max_length=20, db_index=True)
	date = models.DateField(db_index=True)
	data_date = models.DateField(db_index=True)
	# ---營業活動之現金流量－間接法---
	# 繼續營業單位稅前淨利（淨損）
	profit_loss_from_continuing_operations_before_tax = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 本期稅前淨利（淨損）
	profit_loss_before_tax = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 折舊費用
	depreciation_expense = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 攤銷費用
	amortization_expense = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 利息費用
	interest_expense = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 利息收入
	interest_income = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 股份基礎給付酬勞成本
	share_based_payments = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 採用權益法認列之關聯企業及合資損失（利益）之份額
	share_of_profit_loss_of_associates_using_equity_method = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分及報廢不動產、廠房及設備損失（利益）
	loss_gain_on_disposal_of_property_plan_and_equipment = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分投資損失（利益）
	loss_gain_on_disposal_of_investments = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分採用權益法之投資損失（利益）
	loss_gain_on_disposal_of_investments_using_equity_method = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 金融資產減損損失
	impairment_loss_on_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 非金融資產減損損失
	impairment_loss_on_non_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 已實現銷貨損失（利益）
	realized_loss_profit_on_from_sales = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 未實現外幣兌換損失（利益）
	unrealized_foreign_exchange_loss_gain = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他項目
	other_adjustments_to_reconcile_profit_loss = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 不影響現金流量之收益費損項目合計
	total_adjustments_to_reconcile_profit_loss = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 持有供交易之金融資產（增加）減少
	decrease_increase_in_financial_assets_held_for_trading = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 避險之衍生金融資產（增加）減少
	decrease_increase_in_derivative_financial_assets_for_hedging = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應收帳款（增加）減少
	decrease_increase_in_accounts_receivable = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應收帳款－關係人（增加）減少
	decrease_increase_in_accounts_receivable_from_related_parties = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他應收款－關係人（增加）減少
	decrease_increase_in_other_receivable_due_from_related_parties = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存貨（增加）減少
	decrease_increase_in_inventories = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他流動資產（增加）減少
	decrease_increase_in_other_current_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他金融資產（增加）減少
	decrease_increase_in_other_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 與營業活動相關之資產之淨變動合計
	total_changes_in_operating_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應付帳款（增加）減少
	increase_decrease_in_accounts_payable = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應付帳款－關係人（增加）減少
	increase_decrease_in_accounts_payable_to_related_parties = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 負債準備增加（減少）
	increase_decrease_in_provisions = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他流動負債增加（減少）
	increase_decrease_in_other_current_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應計退休金負債增加（減少）
	increase_decrease_in_accrued_pension_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他營業負債增加（減少）
	increase_decrease_in_other_operating_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 與營業活動相關之負債之淨變動合計
	total_changes_in_operating_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 與營業活動相關之資產及負債之淨變動合計
	total_changes_in_operating_assets_and_liabilities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 調整項目合計
	total_adjustments = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 營運產生之現金流入（流出）
	cash_inflow_outflow_generated_from_operations = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 退還（支付）之所得稅
	income_taxes_refund_paid = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 營業活動之淨現金流入（流出）
	net_cash_flows_from_used_in_operating_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# ---投資活動之現金流量---
	# 取得備供出售金融資產
	acquisition_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分備供出售金融資產
	proceeds_from_disposal_of_available_for_sale_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 取得持有至到期日金融資產
	acquisition_of_held_to_maturity_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 持有至到期日金融資產到期還本
	proceeds_from_repayments_of_held_to_maturity_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 取得以成本衡量之金融資產
	acquisition_of_financial_assets_at_cost = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分以成本衡量之金融資產
	proceeds_from_disposal_of_financial_assets_at_cost = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分採用權益法之投資
	proceeds_from_disposal_of_investments_using_equity_method = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分子公司
	proceeds_from_disposal_of_subsidiaries = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 取得不動產、廠房及設備
	acquisition_of_property_plant_and_equipment = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 處分不動產、廠房及設備
	proceeds_from_disposal_of_property_plant_and_equipment = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存出保證金增加
	increase_in_refundable_deposits = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存出保證金減少
	decrease_in_refundable_deposits = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 取得無形資產
	acquisition_of_intangible_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 長期應收租賃款減少 or 應收租賃款減少
	decrease_in_long_term_lease_and_installment_receivables = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他金融資產增加
	increase_in_other_financial_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他非流動資產增加
	increase_in_other_non_current_assets = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 收取之利息
	interest_received = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 收取之股利
	dividends_received = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他投資活動
	other_investing_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 投資活動之淨現金流入（流出）
	net_cash_flows_from_used_in_investing_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# ---籌資活動之現金流量---
	# 短期借款增加
	increase_in_short_term_loans = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 發行公司債
	proceeds_from_issuing_bonds = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 償還公司債
	repayments_of_bonds = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 舉借長期借款
	proceeds_from_long_term_debt = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 償還長期借款
	repayments_of_long_term_debt = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存入保證金增加
	increase_in_guarantee_deposits_received = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 存入保證金減少
	decrease_in_guarantee_deposits_received = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 應付租賃款減少
	decrease_in_lease_payable = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 員工執行認股權
	exercise_of_employee_share_options = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 支付之利息
	interest_paid = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 非控制權益變動
	change_in_non_controlling_interests = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 其他籌資活動
	other_financing_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 籌資活動之淨現金流入（流出）
	net_cash_flows_from_used_in_financing_activities = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 匯率變動對現金及約當現金之影響
	effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 本期現金及約當現金增加（減少）數
	net_increase_decrease_in_cash_and_cash_equivalents = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 期初現金及約當現金餘額
	cash_and_cash_equivalents_at_beginning_of_period = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 期末現金及約當現金餘額
	cash_and_cash_equivalents_at_end_of_period = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 資產負債表帳列之現金及約當現金
	cash_and_cash_equivalents_in_the_statement_of_financial_position = models.DecimalField(max_digits=20 ,decimal_places=0, default=0)
	# 自由現金流量
	free_cash_flow = models.DecimalField(max_digits=20, decimal_places=0, default=0)
# 財務比率表(年)
class YearFinancialRatio(models.Model):
	surrogate_key = models.CharField(max_length=20, primary_key=True)
	year = models.IntegerField(db_index=True)
	symbol = models.CharField(max_length=20, db_index=True)
	date = models.DateField(db_index=True)
	data_date = models.DateField(db_index=True)
	# ---獲利能力---
	# 營業毛利率 = 營業毛利 / 營業收入
	gross_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 營業利益率 = 營業利益 / 營業收入
	operating_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 稅前淨利率 = 稅前純益 / 營業收入
	net_profit_margin_before_tax = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 稅後淨利率 = 稅後純益 / 營業收入
	net_profit_margin = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 每股營業額(元)
	revenue_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
	# 每股營業利益(元)
	operating_profit_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
	# 每股稅前淨利(元)
	net_before_tax_profit_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
	# 每股盈餘(EPS)
	earnings_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
	# 總資產報酬率(ROA)
	return_on_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 股東權益報酬率(ROE) = 本期淨利(稅前) / 期初期末平均之權益總額(期初股東權益+期末股東權益/2)
	return_on_equity = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# ---償債能力---
	# 流動比率
	current_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 速動比率
	quick_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 金融負債比率
	financial_debt_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 負債比率
	debt_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 利息保障倍數
	interest_cover = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	# ---經營能力---
	# 應收帳款週轉率
	accounts_receivable_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 存貨週轉率
	inventory_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 固定資產週轉率
	fixed_asset_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 總資產週轉率
	total_asset_turnover_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# ---黃國華指標---
	# 存貨營收比
	inventory_sales_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 備供出售比率
	available_for_sale_to_equity_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 無形資產比率
	intangible_asset_to_equity_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 折舊負擔比率
	depreciation_to_sales_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 營業利益佔稅前淨利比率
	operating_profit_to_net_profit_before_tax_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 現金股息配發率
	payout_ratio = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	# 營業稅率
	tax_rate = models.DecimalField(max_digits=20, decimal_places=2, null=True)

	modified_date = models.DateField(auto_now=True)

	def __unicode__(self):
		return u'%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (self.ID, self.symbol, self.date, 
			self.gross_profit_margin, self.operating_profit_margin, self.net_profit_margin,
			self.earnings_per_share, self.return_on_assets, self.return_on_equity,
			self.current_ratio, self.quick_ratio, self.financial_debt_ratio, self.debt_ratio,
			self.accounts_receivable_turnover_ratio, self.inventory_turnover_ratio,
			self.fixed_asset_turnover_ratio, self.total_asset_turnover_ratio,
			self.inventory_sales_ratio,self.available_for_sale_to_equity_ratio,
			self.intangible_asset_to_equity_ratio,self.undepreciation_ratio,
			self.depreciation_to_sales_ratio,self.operating_profit_to_net_profit_before_tax_ratio,
			self.payout_ratio , self.tax_rate ,self.modified_date)
	class Meta:
		ordering = ['symbol', 'date']
	class Admin:
		pass