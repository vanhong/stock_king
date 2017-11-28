from django.db import models

# Create your models here.

# 綜合損益表(季)
class SeasonIncomeStatement(models.Model):
	surrogate_key = models.CharField(max_length=50, primary_key=True)
	symbol = models.CharField(max_length=20, db_index=True)
	year = models.IntegerField(db_index=True)
	season = models.IntegerField(db_index=True)
	date = models.DateField(db_index=True)
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
