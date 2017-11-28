#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
import urllib.request
from django.http import HttpResponse
from bs4 import BeautifulSoup
from financial.models import SeasonIncomeStatement
import datetime
import pdb
from decimal import Decimal
import time

# Create your views here.
def season_to_date(year, season):
	if season == 1:
		return datetime.date(year, 1, 1)
	elif season == 2:
		return datetime.date(year, 4, 1)
	elif season == 3:
		return datetime.date(year, 7, 1)
	elif season == 4:
		return datetime.date(year, 10, 1)

def st_to_decimal(data):
	return Decimal(data.strip().replace(',', ''))

def get_updated_id(year, season):
    url = 'http://mops.twse.com.tw/mops/web/t163sb14'
    headers = {'User-Agent': 'Mozilla/5.0'}
    values = {'encodeURIComponent': '1', 'step': '1', 'firstin': '1', 'off': '1', 
              'TYPEK': 'otc', 'year': str(year-1911), 'season': str(season).zfill(2)} 
    url_data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(url, url_data, headers)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        if hasattr(e, "reason"):
            print("get update stockIDs error" + " Reason:"), e.reason
        return []
    soup = BeautifulSoup(response, from_encoding = "utf-8")
    table = soup.find('table', attrs={'class': 'hasBorder'})
    trs = table.find_all('tr')
    company_list = []
    for tr in trs:
        td = tr.find('td')
        if td and len(td.string) == 4:
            company_list.append(td.string)

    values = {'encodeURIComponent': '1', 'step': '1', 'firstin': '1', 'off': '1', 
              'TYPEK': 'sii', 'year': str(year-1911), 'season': str(season).zfill(2)} 
    url_data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(url, url_data, headers)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        if hasattr(e, "reason"):
            print("get update stockIDs error" + " Reason:"), e.reason
        return []
    soup = BeautifulSoup(response, from_encoding = "utf-8")
    table = soup.find('table', attrs={'class': 'hasBorder'})
    trs = table.find_all('tr')
    for tr in trs:
        td = tr.find('td')
        if td and len(td.string) == 4:
            company_list.append(td.string)
    return company_list

def show_season_income_statement(request):
	url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb04'
	headers = {'User-Agent': 'Mozilla/5.0'}
	values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'sii', 'step' : '2',
			   'year' : '103', 'season' : '04', 'co_id' : '8109', 'firstin' : '1'}
	url_data = urllib.parse.urlencode(values).encode('utf-8')
	req = urllib.request.Request(url, url_data, headers)
	response = urllib.request.urlopen(req)
	return HttpResponse(response.read())

#綜合損益表(季)
def update_season_income_statement(request):
	if 'date' in request.GET:
		date = request.GET['date']
		if date != '':
			try:
				str_year, str_season = date.split('-')
				year = int(str_year)
				season = int(str_season)
			except:
				return HttpResponse('please input correct date "year-season"')
		else:
			return HttpResponse('please input correct date "year-season"')
	else:
		return HttpResponse('please input correct date "year-season"')
	print('start update season income statement season:' + str_year + '-' + str_season)
	stockids = get_updated_id(year, season)
	if season == 4:
		incomeStatementSeason1 = SeasonIncomeStatement.objects.filter(year=year, season=1)
		incomeStatementSeason1 = SeasonIncomeStatement.objects.filter(year=year, season=2)
		incomeStatementSeason1 = SeasonIncomeStatement.objects.filter(year=year, season=3)
	headers = {'User-Agent': 'Mozilla/5.0'}
	for symbol in stockids:
		if SeasonIncomeStatement.objects.filter(symbol=symbol, year=year, season=season):
			continue
		url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb04'
		values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'sii', 'step' : '2',
				  'year' : str(year-1911), 'season' : str(season).zfill(2), 'co_id' : symbol, 'firstin' : '1'}
		url_data = urllib.parse.urlencode(values).encode('utf-8')
		req = urllib.request.Request(url, url_data, headers)
		try:
			response = urllib.request.urlopen(req)
			html = response.read()
			#soup = BeautifulSoup(response, from_encoding='utf-8')
			soup = BeautifulSoup(html.decode("utf-8", "ignore"), "html.parser")
			season_income_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
			busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
		except urllib.error.URLError as e:
			time.sleep(20)
			busy_msg = True
			if hasattr(e, 'reason'):
				print(symbol + ' not update. Reason:', e.reason)
		while busy_msg:
			response.close()
			req = urllib.request.Request(url, url_data, headers)
			try:
				response = urllib.request.urlopen(req)
				html = response.read()
				#soup = BeautifulSoup(response, from_encoding='utf-8')
				soup = BeautifulSoup(html.decode("utf-8", "ignore"), "html.parser")
				season_income_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
				busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
			except urllib.error.URLError as e:
				busy_msg = True
				if hasattr(e, 'reason'):
					print(symbol + ' not update. Reason:', e.reason)
			if busy_msg:
				print(symbol + ' sleep 20 seconds')
				time.sleep(20)
		income_statement = SeasonIncomeStatement()
		income_statement.symbol = symbol
		income_statement.year = year
		income_statement.season = season
		income_statement.surrogate_key = symbol + '_' + str(year) + str(season).zfill(2)
		income_statement.date = season_to_date(year, season)
		owners_of_parent = 0
		print(symbol + ' loaded')
		symbolSeason1 = None
		symbolSeason2 = None
		symbolSeason3 = None
		hasPrevSeasons = False
		if season == 4:
			if incomeStatementsSeason1:
				if incomeStatementsSeason1.filter(symbol=symbol):
					symbolSeason1 = incomeStatementsSeason1.get(symbol=symbol)
			if incomeStatementsSeason2:
				if incomeStatementsSeason2.filter(symbol=symbol):
					symbolSeason2 = incomeStatementsSeason2.get(symbol=symbol)
			if incomeStatementsSeason3:
				if incomeStatementsSeason3.filter(symbol=symbol):
					symbolSeason3 = incomeStatementsSeason3.get(symbol=symbol)
			if symbolSeason1 and symbolSeason2 and symbolSeason3:
				hasPrevSeasons = True
		for data in season_income_datas:
			if r'營業收入合計' in data.string or '收入合計' == data.string or '淨收益' == data.string or r'收益合計' == data.string:
				next_data = data.next_sibling.next_sibling
				if not hasPrevSeasons:
					income_statement.total_operating_revenue = st_to_decimal(next_data.string)
				elif symbolSeason1.total_operating_revenue is not None and symbolSeason2.total_operating_revenue is not None and symbolSeason3.total_operating_revenue is not None:
					income_statement.total_operating_revenue = st_to_decimal(next_data.string) - symbolSeason1.total_operating_revenue - symbolSeason2.total_operating_revenue - symbolSeason3.total_operating_revenue
			elif r'營業成本合計' in data.string:
				next_data = data.next_sibling.next_sibling
				if not hasPrevSeasons:
					income_statement.total_operating_cost = st_to_decimal(next_data.string)
				elif symbolSeason1.total_operating_cost is not None and symbolSeason2.total_operating_cost is not None and symbolSeason3.total_operating_cost is not None:
					income_statement.total_operating_cost = st_to_decimal(next_data.string) - symbolSeason1.total_operating_cost - symbolSeason2.total_operating_cost - symbolSeason3.total_operating_cost
			elif r'營業毛利（毛損）' == data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.gross_profit_loss_from_operations = st_to_decimal(next_data.string)
			    elif symbolSeason1.gross_profit_loss_from_operations is not None and symbolSeason2.gross_profit_loss_from_operations is not None and symbolSeason3.gross_profit_loss_from_operations is not None:
			        income_statement.gross_profit_loss_from_operations = st_to_decimal(next_data.string) - symbolSeason1.gross_profit_loss_from_operations - symbolSeason2.gross_profit_loss_from_operations - symbolSeason3.gross_profit_loss_from_operations
			elif r'未實現銷貨（損）益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.unrealized_profit_loss_from_sales = st_to_decimal(next_data.string)
			    elif symbolSeason1.unrealized_profit_loss_from_sales is not None and symbolSeason2.unrealized_profit_loss_from_sales is not None and symbolSeason3.unrealized_profit_loss_from_sales is not None:
			        income_statement.unrealized_profit_loss_from_sales = st_to_decimal(next_data.string) - symbolSeason1.unrealized_profit_loss_from_sales - symbolSeason2.unrealized_profit_loss_from_sales - symbolSeason3.unrealized_profit_loss_from_sales
			elif r'已實現銷貨（損）益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.realized_profit_loss_from_sales = st_to_decimal(next_data.string)
			    elif symbolSeason1.realized_profit_loss_from_sales is not None and symbolSeason2.realized_profit_loss_from_sales is not None and symbolSeason3.realized_profit_loss_from_sales is not None:
			        income_statement.realized_profit_loss_from_sales = st_to_decimal(next_data.string) - symbolSeason1.realized_profit_loss_from_sales - symbolSeason2.realized_profit_loss_from_sales - symbolSeason3.realized_profit_loss_from_sales
			elif r'營業毛利（毛損）淨額' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_gross_profit_from_operations = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_gross_profit_from_operations is not None and symbolSeason2.net_gross_profit_from_operations is not None and symbolSeason3.net_gross_profit_from_operations is not None:
			        income_statement.net_gross_profit_from_operations = st_to_decimal(next_data.string) - symbolSeason1.net_gross_profit_from_operations - symbolSeason2.net_gross_profit_from_operations - symbolSeason3.net_gross_profit_from_operations
			elif r'推銷費用' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.total_selling_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.total_selling_expenses is not None and symbolSeason2.total_selling_expenses is not None and symbolSeason3.total_selling_expenses is not None:
			        income_statement.total_selling_expenses = st_to_decimal(next_data.string) - symbolSeason1.total_selling_expenses - symbolSeason2.total_selling_expenses - symbolSeason3.total_selling_expenses
			elif r'管理費用' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.administrative_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.administrative_expenses is not None and symbolSeason2.administrative_expenses is not None and symbolSeason3.administrative_expenses is not None:
			        income_statement.administrative_expenses = st_to_decimal(next_data.string) - symbolSeason1.administrative_expenses - symbolSeason2.administrative_expenses - symbolSeason3.administrative_expenses
			elif r'研究發展費用' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.research_and_development_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.research_and_development_expenses is not None and symbolSeason2.research_and_development_expenses is not None and symbolSeason3.research_and_development_expenses is not None:
			        income_statement.research_and_development_expenses = st_to_decimal(next_data.string) - symbolSeason1.research_and_development_expenses - symbolSeason2.research_and_development_expenses - symbolSeason3.research_and_development_expenses
			elif r'營業費用合計' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.total_operating_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.total_operating_expenses is not None and symbolSeason2.total_operating_expenses is not None and symbolSeason3.total_operating_expenses is not None:
			        income_statement.total_operating_expenses = st_to_decimal(next_data.string) - symbolSeason1.total_operating_expenses - symbolSeason2.total_operating_expenses - symbolSeason3.total_operating_expenses
			elif r'其他收益及費損淨額' in data.string:
			    if data.next_sibling.next_sibling.string is not None:
			        next_data = data.next_sibling.next_sibling
			        if not hasPrevSeasons:
			            income_statement.net_other_income_expenses = st_to_decimal(next_data.string)
			        elif symbolSeason1.net_other_income_expenses is not None and symbolSeason2.net_other_income_expenses is not None and symbolSeason3.net_other_income_expenses is not None:
			            income_statement.net_other_income_expenses = st_to_decimal(next_data.string) - symbolSeason1.net_other_income_expenses - symbolSeason2.net_other_income_expenses - symbolSeason3.net_other_income_expenses
			elif r'營業利益（損失）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_operating_income_loss = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_operating_income_loss is not None and symbolSeason2.net_operating_income_loss is not None and symbolSeason3.net_operating_income_loss is not None:
			        income_statement.net_operating_income_loss = st_to_decimal(next_data.string) - symbolSeason1.net_operating_income_loss - symbolSeason2.net_operating_income_loss - symbolSeason3.net_operating_income_loss
			elif r'其他收入' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.other_income = st_to_decimal(next_data.string)
			    elif symbolSeason1.other_income is not None and symbolSeason2.other_income is not None and symbolSeason3.other_income is not None:
			        income_statement.other_income = st_to_decimal(next_data.string) - symbolSeason1.other_income - symbolSeason2.other_income - symbolSeason3.other_income
			elif r'其他利益及損失淨額' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.other_gains_and_losses = st_to_decimal(next_data.string)
			    elif symbolSeason1.other_gains_and_losses is not None and symbolSeason2.other_gains_and_losses is not None and symbolSeason3.other_gains_and_losses is not None:
			        income_statement.other_gains_and_losses = st_to_decimal(next_data.string) - symbolSeason1.other_gains_and_losses - symbolSeason2.other_gains_and_losses - symbolSeason3.other_gains_and_losses
			elif r'財務成本淨額' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_finance_costs = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_finance_costs is not None and symbolSeason2.net_finance_costs is not None and symbolSeason3.net_finance_costs is not None:
			        income_statement.net_finance_costs = st_to_decimal(next_data.string) - symbolSeason1.net_finance_costs - symbolSeason2.net_finance_costs - symbolSeason3.net_finance_costs
			elif r'採用權益法認列之關聯企業及合資損益之份額淨額' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.share_of_profit_loss_of_associates_using_equity_method = st_to_decimal(next_data.string)
			    elif symbolSeason1.share_of_profit_loss_of_associates_using_equity_method is not None and symbolSeason2.share_of_profit_loss_of_associates_using_equity_method is not None and symbolSeason3.share_of_profit_loss_of_associates_using_equity_method is not None:
			        income_statement.share_of_profit_loss_of_associates_using_equity_method = st_to_decimal(next_data.string) - symbolSeason1.share_of_profit_loss_of_associates_using_equity_method - symbolSeason2.share_of_profit_loss_of_associates_using_equity_method - symbolSeason3.share_of_profit_loss_of_associates_using_equity_method
			elif r'營業外收入及支出合計' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.total_non_operating_income_and_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.total_non_operating_income_and_expenses is not None and symbolSeason2.total_non_operating_income_and_expenses is not None and symbolSeason3.total_non_operating_income_and_expenses is not None:
			        income_statement.total_non_operating_income_and_expenses = st_to_decimal(next_data.string) - symbolSeason1.total_non_operating_income_and_expenses - symbolSeason2.total_non_operating_income_and_expenses - symbolSeason3.total_non_operating_income_and_expenses
			elif r'稅前淨利（淨損）' in data.string or r'繼續營業單位稅前淨利（淨損）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.profit_loss_from_continuing_operations_before_tax = st_to_decimal(next_data.string)
			    elif symbolSeason1.profit_loss_from_continuing_operations_before_tax is not None and symbolSeason2.profit_loss_from_continuing_operations_before_tax is not None and symbolSeason3.profit_loss_from_continuing_operations_before_tax is not None:
			        income_statement.profit_loss_from_continuing_operations_before_tax = st_to_decimal(next_data.string) - symbolSeason1.profit_loss_from_continuing_operations_before_tax - symbolSeason2.profit_loss_from_continuing_operations_before_tax - symbolSeason3.profit_loss_from_continuing_operations_before_tax
			elif r'所得稅費用（利益）合計' in data.string or r'所得稅（費用）利益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.total_tax_expense = st_to_decimal(next_data.string)
			    elif symbolSeason1.total_tax_expense is not None and symbolSeason2.total_tax_expense is not None and symbolSeason3.total_tax_expense is not None:
			        income_statement.total_tax_expense = st_to_decimal(next_data.string) - symbolSeason1.total_tax_expense - symbolSeason2.total_tax_expense - symbolSeason3.total_tax_expense
			elif r'繼續營業單位本期淨利（淨損）' in data.string or r'繼續營業單位本期稅後淨利（淨損）' in data.string or r'繼續營業單位淨利（淨損）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.profit_loss_from_continuing_operations = st_to_decimal(next_data.string)
			    elif symbolSeason1.profit_loss_from_continuing_operations is not None and symbolSeason2.profit_loss_from_continuing_operations is not None and symbolSeason3.profit_loss_from_continuing_operations is not None:
			        income_statement.profit_loss_from_continuing_operations = st_to_decimal(next_data.string) - symbolSeason1.profit_loss_from_continuing_operations - symbolSeason2.profit_loss_from_continuing_operations - symbolSeason3.profit_loss_from_continuing_operations
			elif r'本期淨利（淨損）' in data.string or r'本期稅後淨利（淨損）' in data.string:
			    if data.next_sibling.next_sibling.string is not None:
			        next_data = data.next_sibling.next_sibling
			        if not hasPrevSeasons:
			            income_statement.profit_loss = st_to_decimal(next_data.string)
			        elif symbolSeason1.profit_loss is not None and symbolSeason2.profit_loss is not None and symbolSeason3.profit_loss is not None:
			            income_statement.profit_loss = st_to_decimal(next_data.string) - symbolSeason1.profit_loss - symbolSeason2.profit_loss - symbolSeason3.profit_loss
			elif r'國外營運機構財務報表換算之兌換差額' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.exchange_differences_on_translation = st_to_decimal(next_data.string)
			    elif symbolSeason1.exchange_differences_on_translation is not None and symbolSeason2.exchange_differences_on_translation is not None and symbolSeason3.exchange_differences_on_translation is not None:
			        income_statement.exchange_differences_on_translation = st_to_decimal(next_data.string) - symbolSeason1.exchange_differences_on_translation - symbolSeason2.exchange_differences_on_translation - symbolSeason3.exchange_differences_on_translation
			elif r'備供出售金融資產未實現評價損益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.unrealised_gains_losses_for_sale_financial_assets = st_to_decimal(next_data.string)
			    elif symbolSeason1.unrealised_gains_losses_for_sale_financial_assets is not None and symbolSeason2.unrealised_gains_losses_for_sale_financial_assets is not None and symbolSeason3.unrealised_gains_losses_for_sale_financial_assets is not None:
			        income_statement.unrealised_gains_losses_for_sale_financial_assets = st_to_decimal(next_data.string) - symbolSeason1.unrealised_gains_losses_for_sale_financial_assets - symbolSeason2.unrealised_gains_losses_for_sale_financial_assets - symbolSeason3.unrealised_gains_losses_for_sale_financial_assets
			elif r'採用權益法認列之關聯企業及合資之其他綜合損益之份額合計' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.total_share_of_other_income_of_associates_using_equity_method = st_to_decimal(next_data.string)
			    elif symbolSeason1.total_share_of_other_income_of_associates_using_equity_method is not None and symbolSeason2.total_share_of_other_income_of_associates_using_equity_method is not None and symbolSeason3.total_share_of_other_income_of_associates_using_equity_method is not None:
			        income_statement.total_share_of_other_income_of_associates_using_equity_method = st_to_decimal(next_data.string) - symbolSeason1.total_share_of_other_income_of_associates_using_equity_method - symbolSeason2.total_share_of_other_income_of_associates_using_equity_method - symbolSeason3.total_share_of_other_income_of_associates_using_equity_method
			elif r'與其他綜合損益組成部分相關之所得稅' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.income_tax_related_of_other_comprehensive_income = st_to_decimal(next_data.string)
			    elif symbolSeason1.income_tax_related_of_other_comprehensive_income is not None and symbolSeason2.income_tax_related_of_other_comprehensive_income is not None and symbolSeason3.income_tax_related_of_other_comprehensive_income is not None:
			        income_statement.income_tax_related_of_other_comprehensive_income = st_to_decimal(next_data.string) - symbolSeason1.income_tax_related_of_other_comprehensive_income - symbolSeason2.income_tax_related_of_other_comprehensive_income - symbolSeason3.income_tax_related_of_other_comprehensive_income
			elif r'其他綜合損益（淨額）' in data.string or r'其他綜合損益（稅後）淨額' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_other_comprehensive_income = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_other_comprehensive_income is not None and symbolSeason2.net_other_comprehensive_income is not None and symbolSeason3.net_other_comprehensive_income is not None:
			        income_statement.net_other_comprehensive_income = st_to_decimal(next_data.string) - symbolSeason1.net_other_comprehensive_income - symbolSeason2.net_other_comprehensive_income - symbolSeason3.net_other_comprehensive_income
			elif r'其他綜合損益' in data.string:
			    if data.next_sibling.next_sibling.string is not None:
			        next_data = data.next_sibling.next_sibling
			        if not hasPrevSeasons:
			            income_statement.other_comprehensive_income = st_to_decimal(next_data.string)
			        elif symbolSeason1.other_comprehensive_income is not None and symbolSeason2.other_comprehensive_income is not None and symbolSeason3.other_comprehensive_income is not None:
			            income_statement.other_comprehensive_income = st_to_decimal(next_data.string) - symbolSeason1.other_comprehensive_income - symbolSeason2.other_comprehensive_income - symbolSeason3.other_comprehensive_income
			elif r'本期綜合損益總額' in data.string or r'本期綜合損益總額（稅後）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.total_comprehensive_income = st_to_decimal(next_data.string)
			    elif symbolSeason1.total_comprehensive_income is not None and symbolSeason2.total_comprehensive_income is not None and symbolSeason3.total_comprehensive_income is not None:
			        income_statement.total_comprehensive_income = st_to_decimal(next_data.string) - symbolSeason1.total_comprehensive_income - symbolSeason2.total_comprehensive_income - symbolSeason3.total_comprehensive_income
			elif r'母公司業主（淨利／損）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.profit_loss_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
			    elif symbolSeason1.profit_loss_attributable_to_owners_of_parent is not None and symbolSeason2.profit_loss_attributable_to_owners_of_parent is not None and symbolSeason3.profit_loss_attributable_to_owners_of_parent is not None:
			        income_statement.profit_loss_attributable_to_owners_of_parent = st_to_decimal(next_data.string) - symbolSeason1.profit_loss_attributable_to_owners_of_parent - symbolSeason2.profit_loss_attributable_to_owners_of_parent - symbolSeason3.profit_loss_attributable_to_owners_of_parent
			elif r'非控制權益（淨利／損）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.profit_loss_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
			    elif symbolSeason1.profit_loss_attributable_to_owners_of_parent is not None and symbolSeason2.profit_loss_attributable_to_owners_of_parent is not None and symbolSeason3.profit_loss_attributable_to_owners_of_parent is not None:
			        income_statement.profit_loss_attributable_to_owners_of_parent = st_to_decimal(next_data.string) - symbolSeason1.profit_loss_attributable_to_owners_of_parent - symbolSeason2.profit_loss_attributable_to_owners_of_parent - symbolSeason3.profit_loss_attributable_to_owners_of_parent
			elif r'母公司業主（綜合損益）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
			    elif symbolSeason1.comprehensive_income_attributable_to_owners_of_parent is not None and symbolSeason2.comprehensive_income_attributable_to_owners_of_parent is not None and symbolSeason3.comprehensive_income_attributable_to_owners_of_parent is not None:
			        income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string) - symbolSeason1.comprehensive_income_attributable_to_owners_of_parent - symbolSeason2.comprehensive_income_attributable_to_owners_of_parent - symbolSeason3.comprehensive_income_attributable_to_owners_of_parent
			elif r'母公司業主' in data.string:
			    if owners_of_parent == 0:
			        next_data = data.next_sibling.next_sibling
			        if not hasPrevSeasons:
			            income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
			        elif symbolSeason1.comprehensive_income_attributable_to_owners_of_parent is not None and symbolSeason2.comprehensive_income_attributable_to_owners_of_parent is not None and symbolSeason3.comprehensive_income_attributable_to_owners_of_parent is not None:
			            income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string) - symbolSeason1.comprehensive_income_attributable_to_owners_of_parent - symbolSeason2.comprehensive_income_attributable_to_owners_of_parent - symbolSeason3.comprehensive_income_attributable_to_owners_of_parent
			        owners_of_parent = 1
			    else:
			        next_data = data.next_sibling.next_sibling
			        if not hasPrevSeasons:
			            income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
			        elif symbolSeason1.comprehensive_income_attributable_to_owners_of_parent is not None and symbolSeason2.comprehensive_income_attributable_to_owners_of_parent is not None and symbolSeason3.comprehensive_income_attributable_to_owners_of_parent is not None:
			            income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string) - symbolSeason1.comprehensive_income_attributable_to_owners_of_parent - symbolSeason2.comprehensive_income_attributable_to_owners_of_parent - symbolSeason3.comprehensive_income_attributable_to_owners_of_parent
			elif r'非控制權益（綜合損益）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.comprehensive_income_attributable_to_non_controlling_interests = st_to_decimal(next_data.string)
			    elif symbolSeason1.comprehensive_income_attributable_to_non_controlling_interests is not None and symbolSeason2.comprehensive_income_attributable_to_non_controlling_interests is not None and symbolSeason3.comprehensive_income_attributable_to_non_controlling_interests is not None:
			        income_statement.comprehensive_income_attributable_to_non_controlling_interests = st_to_decimal(next_data.string) - symbolSeason1.comprehensive_income_attributable_to_non_controlling_interests - symbolSeason2.comprehensive_income_attributable_to_non_controlling_interests - symbolSeason3.comprehensive_income_attributable_to_non_controlling_interests
			elif r'基本每股盈餘' in data.string:
			    if data.next_sibling.next_sibling.string is not None:
			        next_data = data.next_sibling.next_sibling
			        if not hasPrevSeasons:
			            income_statement.total_basic_earnings_per_share = st_to_decimal(next_data.string)
			        elif symbolSeason1.total_basic_earnings_per_share is not None and symbolSeason2.total_basic_earnings_per_share is not None and symbolSeason3.total_basic_earnings_per_share is not None:
			            income_statement.total_basic_earnings_per_share = st_to_decimal(next_data.string) - symbolSeason1.total_basic_earnings_per_share - symbolSeason2.total_basic_earnings_per_share - symbolSeason3.total_basic_earnings_per_share
			elif r'稀釋每股盈餘' in data.string:
			    if data.next_sibling.next_sibling.string is not None:
			        next_data = data.next_sibling.next_sibling
			        if not hasPrevSeasons:
			            income_statement.total_diluted_earnings_per_share = st_to_decimal(next_data.string)
			        elif symbolSeason1.total_diluted_earnings_per_share is not None and symbolSeason2.total_diluted_earnings_per_share is not None and symbolSeason3.total_diluted_earnings_per_share is not None:
			            income_statement.total_diluted_earnings_per_share = st_to_decimal(next_data.string) - symbolSeason1.total_diluted_earnings_per_share - symbolSeason2.total_diluted_earnings_per_share - symbolSeason3.total_diluted_earnings_per_share
			elif r'利息收入' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.interest_income = st_to_decimal(next_data.string)
			    elif symbolSeason1.interest_income is not None and symbolSeason2.interest_income is not None and symbolSeason3.interest_income is not None:
			        income_statement.interest_income = st_to_decimal(next_data.string) - symbolSeason1.interest_income - symbolSeason2.interest_income - symbolSeason3.interest_income
			elif r'減：利息費用' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.interest_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.interest_expenses is not None and symbolSeason2.interest_expenses is not None and symbolSeason3.interest_expenses is not None:
			        income_statement.interest_expenses = st_to_decimal(next_data.string) - symbolSeason1.interest_expenses - symbolSeason2.interest_expenses - symbolSeason3.interest_expenses
			elif r'利息淨收益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_interest_income_expense = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_interest_income_expense is not None and symbolSeason2.net_interest_income_expense is not None and symbolSeason3.net_interest_income_expense is not None:
			        income_statement.net_interest_income_expense = st_to_decimal(next_data.string) - symbolSeason1.net_interest_income_expense - symbolSeason2.net_interest_income_expense - symbolSeason3.net_interest_income_expense
			elif r'手續費淨收益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_service_fee_charge_and_commisions_income_loss = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_service_fee_charge_and_commisions_income_loss is not None and symbolSeason2.net_service_fee_charge_and_commisions_income_loss is not None and symbolSeason3.net_service_fee_charge_and_commisions_income_loss is not None:
			        income_statement.net_service_fee_charge_and_commisions_income_loss = st_to_decimal(next_data.string) - symbolSeason1.net_service_fee_charge_and_commisions_income_loss - symbolSeason2.net_service_fee_charge_and_commisions_income_loss - symbolSeason3.net_service_fee_charge_and_commisions_income_loss
			elif r'透過損益按公允價值衡量之金融資產及負債損益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.gain_loss_on_financial_assets_liabilities_at_fair_value = st_to_decimal(next_data.string)
			    elif symbolSeason1.gain_loss_on_financial_assets_liabilities_at_fair_value is not None and symbolSeason2.gain_loss_on_financial_assets_liabilities_at_fair_value is not None and symbolSeason3.gain_loss_on_financial_assets_liabilities_at_fair_value is not None:
			        income_statement.gain_loss_on_financial_assets_liabilities_at_fair_value = st_to_decimal(next_data.string) - symbolSeason1.gain_loss_on_financial_assets_liabilities_at_fair_value - symbolSeason2.gain_loss_on_financial_assets_liabilities_at_fair_value - symbolSeason3.gain_loss_on_financial_assets_liabilities_at_fair_value
			elif r'保險業務淨收益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_income_loss_of_insurance_operations = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_income_loss_of_insurance_operations is not None and symbolSeason2.net_income_loss_of_insurance_operations is not None and symbolSeason3.net_income_loss_of_insurance_operations is not None:
			        income_statement.net_income_loss_of_insurance_operations = st_to_decimal(next_data.string) - symbolSeason1.net_income_loss_of_insurance_operations - symbolSeason2.net_income_loss_of_insurance_operations - symbolSeason3.net_income_loss_of_insurance_operations
			elif r'投資性不動產損益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.gain_loss_on_investment_property = st_to_decimal(next_data.string)
			    elif symbolSeason1.gain_loss_on_investment_property is not None and symbolSeason2.gain_loss_on_investment_property is not None and symbolSeason3.gain_loss_on_investment_property is not None:
			        income_statement.gain_loss_on_investment_property = st_to_decimal(next_data.string) - symbolSeason1.gain_loss_on_investment_property - symbolSeason2.gain_loss_on_investment_property - symbolSeason3.gain_loss_on_investment_property
			elif r'備供出售金融資產之已實現損益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.realized_gains_on_available_for_sale_financial_assets = st_to_decimal(next_data.string)
			    elif symbolSeason1.realized_gains_on_available_for_sale_financial_assets is not None and symbolSeason2.realized_gains_on_available_for_sale_financial_assets is not None and symbolSeason3.realized_gains_on_available_for_sale_financial_assets is not None:
			        income_statement.realized_gains_on_available_for_sale_financial_assets = st_to_decimal(next_data.string) - symbolSeason1.realized_gains_on_available_for_sale_financial_assets - symbolSeason2.realized_gains_on_available_for_sale_financial_assets - symbolSeason3.realized_gains_on_available_for_sale_financial_assets
			elif r'持有至到期日金融資產之已實現損益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.realized_gains_on_held_to_maturity_financial_assets = st_to_decimal(next_data.string)
			    elif symbolSeason1.realized_gains_on_held_to_maturity_financial_assets is not None and symbolSeason2.realized_gains_on_held_to_maturity_financial_assets is not None and symbolSeason3.realized_gains_on_held_to_maturity_financial_assets is not None:
			        income_statement.realized_gains_on_held_to_maturity_financial_assets = st_to_decimal(next_data.string) - symbolSeason1.realized_gains_on_held_to_maturity_financial_assets - symbolSeason2.realized_gains_on_held_to_maturity_financial_assets - symbolSeason3.realized_gains_on_held_to_maturity_financial_assets
			elif r'兌換損益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.foreign_exchange_gains_losses = st_to_decimal(next_data.string)
			    elif symbolSeason1.foreign_exchange_gains_losses is not None and symbolSeason2.foreign_exchange_gains_losses is not None and symbolSeason3.foreign_exchange_gains_losses is not None:
			        income_statement.foreign_exchange_gains_losses = st_to_decimal(next_data.string) - symbolSeason1.foreign_exchange_gains_losses - symbolSeason2.foreign_exchange_gains_losses - symbolSeason3.foreign_exchange_gains_losses
			elif r'資產減損（損失）迴轉利益淨額' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.impairment_loss_or_reversal_of_impairment_loss_on_assets = st_to_decimal(next_data.string)
			    elif symbolSeason1.impairment_loss_or_reversal_of_impairment_loss_on_assets is not None and symbolSeason2.impairment_loss_or_reversal_of_impairment_loss_on_assets is not None and symbolSeason3.impairment_loss_or_reversal_of_impairment_loss_on_assets is not None:
			        income_statement.impairment_loss_or_reversal_of_impairment_loss_on_assets = st_to_decimal(next_data.string) - symbolSeason1.impairment_loss_or_reversal_of_impairment_loss_on_assets - symbolSeason2.impairment_loss_or_reversal_of_impairment_loss_on_assets - symbolSeason3.impairment_loss_or_reversal_of_impairment_loss_on_assets
			elif r'其他利息以外淨損益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_other_non_interest_incomes_losses = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_other_non_interest_incomes_losses is not None and symbolSeason2.net_other_non_interest_incomes_losses is not None and symbolSeason3.net_other_non_interest_incomes_losses is not None:
			        income_statement.net_other_non_interest_incomes_losses = st_to_decimal(next_data.string) - symbolSeason1.net_other_non_interest_incomes_losses - symbolSeason2.net_other_non_interest_incomes_losses - symbolSeason3.net_other_non_interest_incomes_losses
			elif r'利息以外淨損益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_income_loss_except_interest = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_income_loss_except_interest is not None and symbolSeason2.net_income_loss_except_interest is not None and symbolSeason3.net_income_loss_except_interest is not None:
			        income_statement.net_income_loss_except_interest = st_to_decimal(next_data.string) - symbolSeason1.net_income_loss_except_interest - symbolSeason2.net_income_loss_except_interest - symbolSeason3.net_income_loss_except_interest
			elif r'淨收益' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.net_income_loss = st_to_decimal(next_data.string)
			    elif symbolSeason1.net_income_loss and symbolSeason2.net_income_loss and symbolSeason3.net_income_loss:
			        income_statement.net_income_loss = st_to_decimal(next_data.string) - symbolSeason1.net_income_loss - symbolSeason2.net_income_loss - symbolSeason3.net_income_loss
			elif r'呆帳費用及保證責任準備提存（各項提存）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.total_bad_debts_expense_and_guarantee_liability_provisions = st_to_decimal(next_data.string)
			    elif symbolSeason1.total_bad_debts_expense_and_guarantee_liability_provisions is not None and symbolSeason2.total_bad_debts_expense_and_guarantee_liability_provisions is not None and symbolSeason3.total_bad_debts_expense_and_guarantee_liability_provisions is not None:
			        income_statement.total_bad_debts_expense_and_guarantee_liability_provisions = st_to_decimal(next_data.string) - symbolSeason1.total_bad_debts_expense_and_guarantee_liability_provisions - symbolSeason2.total_bad_debts_expense_and_guarantee_liability_provisions - symbolSeason3.total_bad_debts_expense_and_guarantee_liability_provisions
			elif r'保險負債準備淨變動' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.total_net_change_in_provisions_for_insurance_liabilities = st_to_decimal(next_data.string)
			    elif symbolSeason1.total_net_change_in_provisions_for_insurance_liabilities is not None and symbolSeason2.total_net_change_in_provisions_for_insurance_liabilities is not None and symbolSeason3.total_net_change_in_provisions_for_insurance_liabilities is not None:
			        income_statement.total_net_change_in_provisions_for_insurance_liabilities = st_to_decimal(next_data.string) - symbolSeason1.total_net_change_in_provisions_for_insurance_liabilities - symbolSeason2.total_net_change_in_provisions_for_insurance_liabilities - symbolSeason3.total_net_change_in_provisions_for_insurance_liabilities
			elif r'員工福利費用' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.employee_benefits_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.employee_benefits_expenses is not None and symbolSeason2.employee_benefits_expenses is not None and symbolSeason3.employee_benefits_expenses is not None:
			        income_statement.employee_benefits_expenses = st_to_decimal(next_data.string) - symbolSeason1.employee_benefits_expenses - symbolSeason2.employee_benefits_expenses - symbolSeason3.employee_benefits_expenses
			elif r'折舊及攤銷費用' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.employee_benefits_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.employee_benefits_expenses is not None and symbolSeason2.employee_benefits_expenses is not None and symbolSeason3.employee_benefits_expenses is not None:
			        income_statement.employee_benefits_expenses = st_to_decimal(next_data.string) - symbolSeason1.employee_benefits_expenses - symbolSeason2.employee_benefits_expenses - symbolSeason3.employee_benefits_expenses
			elif r'其他業務及管理費用' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.other_general_and_administrative_expenses = st_to_decimal(next_data.string)
			    elif symbolSeason1.other_general_and_administrative_expenses is not None and symbolSeason2.other_general_and_administrative_expenses is not None and symbolSeason3.other_general_and_administrative_expenses is not None:
			        income_statement.other_general_and_administrative_expenses = st_to_decimal(next_data.string) - symbolSeason1.other_general_and_administrative_expenses - symbolSeason2.other_general_and_administrative_expenses - symbolSeason3.other_general_and_administrative_expenses
			elif r'現金流量避險中屬有效避險不分之避險工具利益（損失）' in data.string:
			    next_data = data.next_sibling.next_sibling
			    if not hasPrevSeasons:
			        income_statement.gain_loss_on_effective_portion_of_cash_flow_hedges = st_to_decimal(next_data.string)
			    elif symbolSeason1.gain_loss_on_effective_portion_of_cash_flow_hedges is not None and symbolSeason2.gain_loss_on_effective_portion_of_cash_flow_hedges is not None and symbolSeason3.gain_loss_on_effective_portion_of_cash_flow_hedges is not None:
			        income_statement.gain_loss_on_effective_portion_of_cash_flow_hedges = st_to_decimal(next_data.string) - symbolSeason1.gain_loss_on_effective_portion_of_cash_flow_hedges - symbolSeason2.gain_loss_on_effective_portion_of_cash_flow_hedges - symbolSeason3.gain_loss_on_effective_portion_of_cash_flow_hedges
			elif r'停業單位損益' in data.string or r'停業單位損益合計' in data.string:
			    if data.next_sibling.next_sibling.string is not None:
			        next_data = data.next_sibling.next_sibling
			        if not hasPrevSeasons:
			            income_statement.income_from_discontinued_operations = st_to_decimal(next_data.string)
			        elif symbolSeason1.income_from_discontinued_operations is not None and symbolSeason2.income_from_discontinued_operations is not None and symbolSeason3.income_from_discontinued_operations is not None:
			            income_statement.income_from_discontinued_operations = st_to_decimal(next_data.string) - symbolSeason1.income_from_discontinued_operations - symbolSeason2.income_from_discontinued_operations - symbolSeason3.income_from_discontinued_operations
		if income_statement.total_basic_earnings_per_share is not None:
			income_statement.save()
			print(symbol + ' data updated')
		else:
			time.sleep(20)
			print(symbol + 'has no data-----------')
	cnt = SeasonIncomeStatement.objects.filter(year=year, season=season).count()
	print('There is ' + str(cnt) + ' datas')
	return HttpResponse('update_season_income_statement')

#資產負債表
def show_season_balance_sheet(reqeuest):
	url = 'http://mops.twse.com.tw/mops/web/t164sb03'
	headers = {'User-Agent': 'Mozilla/5.0'}
	values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'all', 'step' : '2',
			  'year' : str(2013-1911), 'season' : str(1).zfill(2), 'co_id' : '6202', 'firstin' : '1'}
	url_data = urllib.parse.urlencode(values).encode('utf-8')
	req = urllib.request.Request(url, url_data, headers)
	response = urllib.request.urlopen(req)
	return HttpResponse(response.read())

def update_season_balance_sheet(request):
	if 'date' in request.GET:
		date = request.GET['date']
	print('start update season balance sheet')