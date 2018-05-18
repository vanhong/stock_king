#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
import urllib.request
from django.http import HttpResponse
from django.db.models import Sum, Max
from bs4 import BeautifulSoup
from financial.models import *
from stocks.models import UpdateManagement
from core.util import *
import datetime
import pdb
from decimal import Decimal
import time
import html
import json

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

def year_to_date(year):
	return datetime.date(year, 1, 1)

def st_to_decimal(data):
	decimal_string = data.strip().replace(',', '')
	if is_numbers(decimal_string):
		return Decimal(decimal_string)
	else:
		return 0

def is_numbers(s):
	try:
		float(s)
		return True
	except ValueError:
		pass
	return False

def prev_season(year, season):
	if season == 1:
		return year-1, 4
	else:
		return year, season-1

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

def old_show_season_income_statement(request):
	url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb04'
	headers = {'User-Agent': 'Mozilla/5.0'}
	values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'sii', 'step' : '2',
			   'year' : '103', 'season' : '04', 'co_id' : '8109', 'firstin' : '1'}
	url_data = urllib.parse.urlencode(values).encode('utf-8')
	req = urllib.request.Request(url, url_data, headers)
	response = urllib.request.urlopen(req)
	return HttpResponse(response.read())

def show_season_income_statement(request):
	url = 'http://mops.twse.com.tw/mops/web/t163sb04'
	headers = {'User-Agent': 'Mozilla/5.0'}
	values = {'encodeURIComponent' : '1', 'step':'1', 'firstin':'1', 'off':'1', 'TYPEK':'otc', 'year':'106', 'season':'1'}
	url_data = urllib.parse.urlencode(values).encode('utf-8')
	req = urllib.request.Request(url, url_data, headers)
	response = urllib.request.urlopen(req)
	return HttpResponse(response.read())

def new_update_season_income_statement(request):
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
	url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb04'
	headers = {'User-Agent': 'Mozilla/5.0'}
	market = ['sii', 'otc']
	for mkt in market:
		values = {'encodeURIComponent' : '1', 'step':'1', 'firstin':'1', 'off':'1', 'TYPEK':mkt, 'year':str(year-1911), 'season':str(season).zfill(1)}
		url_data = urllib.parse.urlencode(values).encode('utf-8')
		req = urllib.request.Request(url, url_data, headers)
		response = urllib.request.urlopen(req)
		soup = BeautifulSoup(response, "html.parser")
		season_income_datas = soup.find_all("table", {'class': 'hasBorder'})
		if season >= 2:
			incomeStatementsSeason1 = SeasonIncomeStatement.objects.filter(year=year, season=1)
			if season >= 3:
				incomeStatementsSeason2 = SeasonIncomeStatement.objects.filter(year=year, season=2)
				if season >= 4:
					incomeStatementsSeason3 = SeasonIncomeStatement.objects.filter(year=year, season=3)
		for data in season_income_datas:
			data_head_sets = data.find_all("tr", {'class', 'tblHead'})
			# 記錄目前header數到哪
			data_head_count = 0
			data_header_dic = {}
			data_header_dic[0] = 'symbol'
			for data_head_set in data_head_sets:
				data_heads = data_head_set.find_all('th')
				for data_head in data_heads:
					if data_head.string in SeasonIncomeStatementTable.SeasonIncomeStatementDic:
						data_header_dic[data_head_count] = SeasonIncomeStatementTable.SeasonIncomeStatementDic[data_head.string]
					data_head_count = data_head_count + 1
			data_body_sets = data.find_all("tr", {'class' : ['even', 'odd']})
			for data_body_set in data_body_sets:
				income_statement = SeasonIncomeStatement()
				data_bodys = data_body_set.find_all('td')
				data_body_count = 0
				income_statement.year = year
				income_statement.season = season
				income_statement.date = season_to_date(year, season)
				for data_body in data_bodys:
					if (data_body_count == 0):
						symbol = data_body.string
						print(symbol + ' loaded')
						income_statement.surrogate_key = symbol + '_' + str(year) + str(season).zfill(2)
						#Q4要扣除前三季的資料
						symbolSeason1 = None
						symbolSeason2 = None
						symbolSeason3 = None
						hasPrevSeasons = False
						if season >= 2:
							if incomeStatementsSeason1:
								if incomeStatementsSeason1.filter(symbol=symbol):
									symbolSeason1 = incomeStatementsSeason1.get(symbol=symbol)
							if season >= 3:
								if incomeStatementsSeason2:
									if incomeStatementsSeason2.filter(symbol=symbol):
										symbolSeason2 = incomeStatementsSeason2.get(symbol=symbol)
								if season >= 4:
									if incomeStatementsSeason3:
										if incomeStatementsSeason3.filter(symbol=symbol):
											symbolSeason3 = incomeStatementsSeason3.get(symbol=symbol)
						if season == 2:
							if symbolSeason1:
								hasPrevSeasons = True
						elif season == 3:
							if symbolSeason1 and symbolSeason2:
								hasPrevSeasons = True
						elif season == 4:
							if symbolSeason1 and symbolSeason2 and symbolSeason3:
								hasPrevSeasons = True
					if (data_body_count in data_header_dic):
						if (data_body_count > 1):
							if not hasPrevSeasons:
								setattr(income_statement, data_header_dic[data_body_count], st_to_decimal(data_body.string))
							else:
								pre_value = 0
								if season == 2:
									season1_value = getattr(symbolSeason1, data_header_dic[data_body_count])
									if season1_value is not None:
										pre_value = season1_value
								elif season == 3:
									season1_value = getattr(symbolSeason1, data_header_dic[data_body_count])
									if season1_value is not None:
										pre_value = pre_value + season1_value
									season2_value = getattr(symbolSeason2, data_header_dic[data_body_count])
									if season2_value is not None:
										pre_value = pre_value + season2_value
								elif season == 4:
									season1_value = getattr(symbolSeason1, data_header_dic[data_body_count])
									if season1_value is not None:
										pre_value = pre_value + season1_value
									season2_value = getattr(symbolSeason2, data_header_dic[data_body_count])
									if season2_value is not None:
										pre_value = pre_value + season2_value
									season3_value = getattr(symbolSeason3, data_header_dic[data_body_count])
									if season2_value is not None:
										pre_value = pre_value + season3_value
								data_value = st_to_decimal(data_body.string) - pre_value
								setattr(income_statement, data_header_dic[data_body_count], data_value)
						else:
							setattr(income_statement, data_header_dic[data_body_count], data_body.string)
					data_body_count = data_body_count + 1
				income_statement.save()
	return HttpResponse('update season income statement season:' + str_year + '-' + str_season)

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
	stockids = get_updated_id(year, season)
	if season == 4:
		incomeStatementsSeason1 = SeasonIncomeStatement.objects.filter(year=year, season=1)
		incomeStatementsSeason2 = SeasonIncomeStatement.objects.filter(year=year, season=2)
		incomeStatementsSeason3 = SeasonIncomeStatement.objects.filter(year=year, season=3)
	headers = {'User-Agent': 'Mozilla/5.0'}
	update_cnt = 0
	for symbol in stockids:
		update_cnt += 1
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
		print ('season income statement:' + symbol + ' loaded '+ str(update_cnt) + ' in ' + str(len(stockids)))
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
			income_statement.data_date = financial_date_to_data_date(year, season)
			income_statement.save()
			print(symbol + ' data updated')
		else:
			time.sleep(20)
			print(symbol + 'has no data-----------')
	cnt = SeasonIncomeStatement.objects.filter(year=year, season=season).count()
	print('There is ' + str(cnt) + ' datas')
	lastDate = SeasonIncomeStatement.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = SeasonIncomeStatement.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='sis', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " sis in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(season)})

	return HttpResponse(json_obj, content_type="application/json")

#資產負債表
def show_season_balance_sheet(reqeuest):
	url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'
	headers = {'User-Agent': 'Mozilla/5.0'}
	values = {'encodeURIComponent' : '1', 'step':'1', 'firstin':'1', 'off':'1', 'TYPEK':'sii', 'year':'106', 'season':'1'}
	url_data = urllib.parse.urlencode(values).encode('utf-8')
	req = urllib.request.Request(url, url_data, headers)
	response = urllib.request.urlopen(req)
	soup = BeautifulSoup(response, "html.parser")
	return HttpResponse(soup)

def new_update_season_balance_sheet(request):
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
	url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'
	headers = {'User-Agent': 'Mozilla/5.0'}
	market = ['sii', 'otc']
	for mkt in market:
		values = {'encodeURIComponent' : '1', 'step':'1', 'firstin':'1', 'off':'1', 'TYPEK':mkt, 'year':str(year-1911), 'season':str(season).zfill(2)}
		url_data = urllib.parse.urlencode(values).encode('utf-8')
		req = urllib.request.Request(url, url_data, headers)
		response = urllib.request.urlopen(req)
		soup = BeautifulSoup(response, "html5lib", from_encoding='utf-8')
		season_balance_datas = soup.find_all("table", {'class': 'hasBorder'})
		#data_body_sets = soup.find_all("tr", {'class' : ['even', 'odd']})
		for data in season_balance_datas:
			data_head_sets = data.find_all("tr", {'class', 'tblHead'})
			# 記錄目前header數到哪
			data_head_count = 0
			data_header_dic = {}
			data_header_dic[0] = 'symbol'
			for data_head_set in data_head_sets:
				data_heads = data_head_set.find_all('th')


				for data_head in data_heads:
					if data_head.string in SeasonBalanceSheetTable.SeasonBalanceSheetDic:
						data_header_dic[data_head_count] = SeasonBalanceSheetTable.SeasonBalanceSheetDic[data_head.string]
					data_head_count = data_head_count + 1
			data_body_sets = data.find_all("tr", {'class' : ['even', 'odd']})
			for data_body_set in data_body_sets:
				balance_sheet = SeasonBalanceSheet()
				data_bodys = data_body_set.find_all('td')
				data_body_count = 0
				balance_sheet.year = year
				balance_sheet.season = season
				balance_sheet.date = season_to_date(year, season)
				for data_body in data_bodys:
					if (data_body_count == 0):
						symbol = data_body.string
						print(symbol + ' loaded')
						balance_sheet.surrogate_key = symbol + '_' + str(year) + str(season).zfill(2)
					if (data_body_count in data_header_dic):
						if (data_body_count > 1):
							setattr(balance_sheet, data_header_dic[data_body_count], st_to_decimal(data_body.string))
						else:
							setattr(balance_sheet, data_header_dic[data_body_count], data_body.string)
					data_body_count = data_body_count + 1
				balance_sheet.save()
	return HttpResponse('update season balance sheet season:' + str_year + '-' + str_season)

#資產負債表(季)--不用年的資料，因為是存量的觀念
def update_season_balance_sheet(request):
	print ('start update season balance sheet')
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
	stockIDs = get_updated_id(year, season)
	update_cnt = 0
	for stock_id in stockIDs:
		update_cnt += 1
		stock_symbol = stock_id
		if not SeasonBalanceSheet.objects.filter(symbol=stock_symbol, year=year, season=season):
			print (stock_symbol + ' loaded '+ str(update_cnt) + ' in ' + str(len(stockIDs)))
			url = 'http://mops.twse.com.tw/mops/web/t164sb03'
			# if stock_symbol[:2] == '28' or stock_symbol == '5880' or stock_symbol == '5820' or stock_symbol == '3990' or stock_symbol == '5871':
			headers = {'User-Agent': 'Mozilla/5.0'}
			values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'all', 'step' : '2',
						'year' : str(year-1911), 'season' : str(season).zfill(1), 'co_id' : stock_symbol, 'firstin' : '1'}
			url_data = urllib.parse.urlencode(values).encode('utf-8')
			req = urllib.request.Request(url, url_data, headers)
			try:
				response = urllib.request.urlopen(req)
				html = response.read()
				soup = BeautifulSoup(html.decode("utf-8", "ignore"), "html.parser")
				balance_sheet_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
				busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
			except urllib.error.URLError as e:
				print (stock_symbol + ' time sleep')
				time.sleep(20)
				busy_msg = True
				if hasattr(e, "reason"):
					print(stock_symbol + " Reason:"), e.reason
				elif hasattr(e, "code"):
					print(stock_symbol + " Error code:"), e.code
			# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
			while (busy_msg is not None):
				response.close()
				headers = {'User-Agent': 'Mozilla/5.0'}
				req = urllib.request.Request(url, url_data, headers)
				try:
					response = urllib.request.urlopen(req)
					html = response.read()
					soup = BeautifulSoup(html.decode("utf-8", "ignore"), "html.parser")
					balance_sheet_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
					busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
				except urllib.error.URLError as e:
					busy_msg = True
					if hasattr(e, "reason"):
						print(stock_symbol + " Reason:"), e.reason
					elif hasattr(e, "code"):
						print(stock_symbol + " Error code:"), e.code
				if busy_msg:
					print (stock_symbol + ' time sleep')
					time.sleep(20)
			balance_sheet = SeasonBalanceSheet()
			balance_sheet.symbol = stock_symbol
			balance_sheet.year = str(year)
			balance_sheet.season = season
			balance_sheet.date = season_to_date(year, season)
			balance_sheet.surrogate_key = stock_symbol + '_' + str(year) + str(season).zfill(2)
			for data in balance_sheet_datas:
				if r'現金及約當現金' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_cash_and_cash_equivalents = st_to_decimal(next_data.string)
				elif r'無活絡市場之債券投資' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_bond_investment_without_active_market = st_to_decimal(next_data.string)
				elif r'透過損益按公允價值衡量之金融資產－流動' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_financial_assets_at_fair_value_through_profit_or_loss = st_to_decimal(next_data.string)
				elif r'備供出售金融資產－流動淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_available_for_sale_financial_assets = st_to_decimal(next_data.string)
				elif r'持有至到期日金融資產－流動淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_held_to_maturity_financial_assets = st_to_decimal(next_data.string)
				elif r'應收票據淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.notes_receivable = st_to_decimal(next_data.string)
				elif r'應收票據－關係人淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.notes_receivable_due_from_related_parties = st_to_decimal(next_data.string)
				elif r'應收帳款淨額' in data.string or r'應收款項淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.accounts_receivable = st_to_decimal(next_data.string)
				elif r'應收帳款－關係人淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.accounts_receivable_due_from_related_parties = st_to_decimal(next_data.string)
				elif r'其他應收款淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_other_receivables = st_to_decimal(next_data.string)
				elif r'其他應收款－關係人淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.other_receivables_due_from_related_parties = st_to_decimal(next_data.string)
				elif r'當期所得稅資產' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_current_tax_assets = st_to_decimal(next_data.string)
				elif r'存貨' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_inventories = st_to_decimal(next_data.string)
				elif r'生物資產－流動淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_biological_asset = st_to_decimal(next_data.string)
				elif r'預付款項' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_prepayments = st_to_decimal(next_data.string)
				elif r'其他流動資產' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_other_current_assets = st_to_decimal(next_data.string)
				elif r'流動資產合計' in data.string and r'非' not in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_current_assets = st_to_decimal(next_data.string)
				elif r'備供出售金融資產－非流動淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.non_current_available_for_sale_financial_assets = st_to_decimal(next_data.string)
				elif r'持有至到期日金融資產－非流動淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.non_current_held_to_maturity_financial_assets_net = st_to_decimal(next_data.string)
				elif r'避險之衍生金融資產－非流動' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.derivative_non_current_financial_assets_for_hedging = st_to_decimal(next_data.string)
				elif r'以成本衡量之金融資產－非流動淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.non_current_financial_assets_at_cost = st_to_decimal(next_data.string)
				elif r'採用權益法之投資淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.investment_accounted_for_using_equity_method = st_to_decimal(next_data.string)
				elif r'不動產、廠房及設備' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_property_plant_and_equipment = st_to_decimal(next_data.string)
				elif r'投資性不動產淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_investment_property = st_to_decimal(next_data.string)
				elif r'無形資產' in data.string:
					next_data = data.next_sibling.next_sibling
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						balance_sheet.intangible_assets = st_to_decimal(next_data.string)
				elif r'遞延所得稅資產' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.deferred_tax_assets = st_to_decimal(next_data.string)
				elif r'其他非流動資產' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_other_non_current_assets = st_to_decimal(next_data.string)
				elif r'非流動資產合計' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_non_current_assets = st_to_decimal(next_data.string)
				elif r'資產總額' in data.string or r'資產總計' in data.string or r'資產合計' == data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_assets = st_to_decimal(next_data.string)
				elif r'短期借款' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_short_term_borrowings = st_to_decimal(next_data.string)
				elif r'應付短期票券' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.short_term_notes_and_bills_payable = st_to_decimal(next_data.string)
				elif r'透過損益按公允價值衡量之金融負債－流動' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_financial_liabilities_fair_value = st_to_decimal(next_data.string)
				elif r'透過損益按公允價值衡量之金融負債－非流動' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.non_current_financial_liabilities_fair_value = st_to_decimal(next_data.string)
				elif r'避險之衍生金融負債－流動' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_derivative_financial_liabilities_for_hedging = st_to_decimal(next_data.string)
				elif r'應付票據' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_notes_payable = st_to_decimal(next_data.string)
				elif r'應付帳款' in data.string or r'應付款項' in data.string and len(data.string.strip()) == 4:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						balance_sheet.total_accounts_payable = st_to_decimal(next_data.string)
				elif r'應付帳款－關係人' in data.string and len(data.string.strip()) == 8:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_accounts_payable_to_related_parties = st_to_decimal(next_data.string)
				elif r'應付建造合約款' in data.string and len(data.string.strip())==7:
					next_data = data.next_sibling.next_sibling
					balance_sheet.construction_contracts_payable = st_to_decimal(next_data.string)
				elif r'應付建造合約款－關係人' in data.string and len(data.string.strip()) == 11:
					next_data = data.next_sibling.next_sibling
					balance_sheet.other_payables_to_related_parties = st_to_decimal(next_data.string)
				elif r'其他應付款' in data.string and len(data.string.strip()) == 5:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_other_payables = st_to_decimal(next_data.string)
				elif r'其他應付款項－關係人' in data.string and len(data.string.strip()) == 10:
					next_data = data.next_sibling.next_sibling
					balance_sheet.other_payables_to_related_parties = st_to_decimal(next_data.string)
				elif r'當期所得稅負債' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_tax_liabilities = st_to_decimal(next_data.string)
				elif r'負債準備－流動' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.current_provisions = st_to_decimal(next_data.string)
				elif r'其他流動負債' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_other_current_liabilities = st_to_decimal(next_data.string)
				elif r'流動負債合計' in data.string and r'非' not in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_current_liabilities = st_to_decimal(next_data.string)
				elif r'避險之衍生金融負債－非流動' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.non_current_derivative_financial_liabilities_for_hedeging = st_to_decimal(next_data.string)
				elif r'應付公司債' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_bonds_payable = st_to_decimal(next_data.string)
				elif r'長期借款' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_long_term_borrowings = st_to_decimal(next_data.string)
				elif r'負債準備－非流動' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_non_current_provisions = st_to_decimal(next_data.string)
				elif r'遞延所得稅負債' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_deferred_tax_liabilities = st_to_decimal(next_data.string)
				elif r'其他非流動負債' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.other_non_current_liabilities = st_to_decimal(next_data.string)
				elif r'非流動負債合計' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_non_current_liabilities = st_to_decimal(next_data.string)
				elif r'負債總額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_liabilities = st_to_decimal(next_data.string)
				elif r'普通股股本' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.ordinary_share = st_to_decimal(next_data.string)
				elif r'預收股本' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.advance_receipts_for_share_capital = st_to_decimal(next_data.string)
				elif r'資本公積－發行溢價' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.additional_paid_in_capital = st_to_decimal(next_data.string)
				elif r'資本公積－取得或處分子公司股權價格與帳面價值差額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.capital_surplus_difference_between_consideration = st_to_decimal(next_data.string)
				elif r'資本公積－受贈資產' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_capital_surplus_donated_assets_received = st_to_decimal(next_data.string)
				elif r'資本公積－採用權益法認列關聯企業及合資股權淨值之變動數' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.capital_surplus_changes_in_equity_of_associates = st_to_decimal(next_data.string)
				elif r'資本公積－庫藏股票交易' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.treasury_share_transactions = st_to_decimal(next_data.string)
				elif r'資本公積－合併溢額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_assets_from_merger = st_to_decimal(next_data.string)
				elif r'資本公積－其他' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.other_capital_surplus = st_to_decimal(next_data.string)
				elif r'資本公積合計' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_capital_surplus = st_to_decimal(next_data.string)
				elif r'法定盈餘公積' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.legal_reserve = st_to_decimal(next_data.string)
				elif r'特別盈餘公積' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.special_reserve = st_to_decimal(next_data.string)
				elif r'未分配盈餘（或待彌補虧損）' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_unappropriated_retained_earnings_or_accumulated_deficit = st_to_decimal(next_data.string)
				elif r'保留盈餘合計' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_retained_earnings = st_to_decimal(next_data.string)
				elif r'其他權益合計' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_other_equity_interest = st_to_decimal(next_data.string)
				elif r'國外營運機構財務報表換算之兌換差額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.exchange_differences_of_foreign_financial_statements = st_to_decimal(next_data.string)
				elif r'備供出售金融資產未實現損益' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.unrealised_gains_for_sale_financial_assets = st_to_decimal(next_data.string)
				elif r'庫藏股票' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.treasury_share = st_to_decimal(next_data.string)
				elif r'歸屬於母公司業主之權益合計' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_equity_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
				elif r'共同控制下前手權益' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.equity_attributable_to_former_owner_of_business_combination = st_to_decimal(next_data.string)
				elif r'非控制權益' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.non_controlling_interests = st_to_decimal(next_data.string)
				elif r'權益總額' in data.string or r'權益總計' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_equity = st_to_decimal(next_data.string)
				elif r'待註銷股本股數（單位：股）' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.number_of_shares_capital_awaiting_retirement = st_to_decimal(next_data.string)
				elif r'預收股款（權益項下）之約當發行股數（單位：股）' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.equivalent_issue_shares_of_advance_receipts = st_to_decimal(next_data.string)
				elif r'母公司暨子公司所持有之母公司庫藏股股數（單位：股）' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.number_of_shares_in_entity_held_by_entity = st_to_decimal(next_data.string)
				elif r'存放央行及拆款同業' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.due_from_the_central_bank_and_call_loans_to_banks = st_to_decimal(next_data.string)
				elif r'避險之衍生金融資產' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.derivative_financial_assets_for_hedging = st_to_decimal(next_data.string)
				elif r'待出售資產－淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_assets_classified_as_held_for_sale = st_to_decimal(next_data.string)
				elif r'貼現及放款－淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_loans_discounted = st_to_decimal(next_data.string)
				elif r'再保險合約資產－淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_reinsurance_contract_assets = st_to_decimal(next_data.string)
				elif r'其他金融資產－淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_other_financial_assets = st_to_decimal(next_data.string)
				elif r'不動產及設備－淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_property_and_equipment = st_to_decimal(next_data.string)
				elif r'其他資產－淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_other_assets = st_to_decimal(next_data.string)
				elif r'央行及金融同業存款' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.deposits_from_the_central_bank_and_banks = st_to_decimal(next_data.string)
				elif r'央行及同業融資' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.due_to_the_central_bank_and_banks = st_to_decimal(next_data.string)
				elif r'附買回票券及債券負債' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.securities_sold_under_repurchase_agreements = st_to_decimal(next_data.string)
				elif r'應付商業本票－淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.net_commercial_papers_issued = st_to_decimal(next_data.string)
				elif r'存款及匯款' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.deposits = st_to_decimal(next_data.string)
				elif r'負債準備' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						balance_sheet.total_provisions = st_to_decimal(next_data.string)
				elif r'其他金融負債' in data.string:
					next_data = data.next_sibling.next_sibling
					balance_sheet.total_other_financial_liabilities = st_to_decimal(next_data.string)
				elif r'股本合計' in data.string or r'股本' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						balance_sheet.total_capital_stock = st_to_decimal(next_data.string)
				elif r'其他負債' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						balance_sheet.total_other_liabilities = st_to_decimal(next_data.string)
				else:
					if data.next_sibling.next_sibling.string is not None:
						pass
						# pdb.set_trace()
			if balance_sheet.total_cash_and_cash_equivalents:
				balance_sheet.data_date = financial_date_to_data_date(year, season)
				balance_sheet.save()
			else:
				print (stock_symbol + ' time sleep')
				time.sleep(5)

			print ('season balance sheet:' + stock_symbol + ' data updated ' + str(update_cnt) + ' in ' + str(len(stockIDs)))
	cnt = SeasonBalanceSheet.objects.filter(year=year, season=season).count()
	lastDate = SeasonBalanceSheet.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = SeasonBalanceSheet.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='scs', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " scs in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(season)})

	return HttpResponse(json_obj, content_type="application/json")

#現金流量表(季)
def show_season_cashflow_statement(reqquest):
	url = 'http://mops.twse.com.tw/mops/web/t164sb05'
	year = 102
	season = 2
	headers = {'User-Agent': 'Mozilla/5.0'}
	values = {'encodeURIComponent' : '1', 'step' : '1', 'firstin' : '1', 'off' : '1',
			'keyword4' : '','code1' : '','TYPEK2' : '','checkbtn' : '',
			'queryName':'co_id', 'TYPEK':'all', 'isnew':'true', 'co_id' : 8109, 'year' : year, 'season' : str(season).zfill(2) }
	# values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'all', 'step' : '2',
	#			'year' : '102', 'season' : '2', 'co_id' : stock_symbol, 'firstin' : '1'}
	url_data = urllib.parse.urlencode(values).encode('utf-8')
	req = urllib.request.Request(url, url_data, headers)
	response = urllib.request.urlopen(req)
	soup = BeautifulSoup(response, "html.parser")
	# print soup 詳細資料
	detail_button = soup.find_all("input", {'type': 'button', 'value': r'詳細資訊'})
	print (detail_button)

	# balance_sheet_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
	# for data in balance_sheet_datas:
	#	if r'現金及約當現金' in data.string.encode('utf-8'):
	#		next_data = data.next_sibling.next_sibling
	#		print st_to_decimal(next_data.string)
	#		next_data = next_data.next_sibling.next_sibling.next_sibling.next_sibling
	#		print st_to_decimal(next_data.string)
	#req = urllib2.Request(url, url_data)
	#response = urllib2.urlopen(req)
	return HttpResponse(soup)

#現金流量表(季)
def update_season_cashflow_statement(request):
	print ('start update season cashflow statement')
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
	stockIDs = get_updated_id(year, season)
	update_cnt = 0
	for stock_symbol in stockIDs:
		update_cnt += 1
		if not SeasonCashflowStatement.objects.filter(symbol=stock_symbol, year=year, season=season):
			print ('season cashflow:' + stock_symbol + ' loaded '+ str(update_cnt) + ' in ' + str(len(stockIDs)))
			url = 'http://mops.twse.com.tw/mops/web/t164sb05'
			headers = {'User-Agent': 'Mozilla/5.0'}
			values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'all', 'step' : '2',
					'year' : str(year-1911), 'season' : str(season).zfill(1), 'co_id' : stock_symbol, 'firstin' : '1'}
			url_data = urllib.parse.urlencode(values).encode('utf-8')
			req = urllib.request.Request(url, url_data, headers)
			try:
				response = urllib.request.urlopen(req)
				html = response.read()
				soup = BeautifulSoup(html.decode("utf-8", "ignore"), "html5lib")
				cashflows_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
				busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
			except urllib.error.URLError as e:
				print (stock_symbol + ' time sleep')
				time.sleep(20)
				busy_msg = True
				if hasattr(e, "reason"):
					print(stock_symbol + " Reason:"), e.reason
				elif hasattr(e, "code"):
					print(stock_symbol + " Error code:"), e.code
			# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
			while (busy_msg is not None):
				#response.close()
				headers = {'User-Agent': 'Mozilla/5.0'}
				req = urllib.request.Request(url, url_data, headers)
				try:
					response = urllib.request.urlopen(req)
					html = response.read()
					soup = BeautifulSoup(html.decode('utf-8', 'ignore'), "html5lib")
					cashflows_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
					busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
				except urllib.error.URLError as e:
					busy_msg = True
					if hasattr(e, "reason"):
						print(stock_symbol + " Reason:"), e.reason
					elif hasattr(e, "code"):
						print(stock_symbol + " Error code:"), e.code
				if busy_msg:
					print (stock_symbol + ' time sleep')
					time.sleep(20)
			cashflow = SeasonCashflowStatement()
			cashflow.symbol = stock_symbol
			cashflow.year = str(year)
			cashflow.season = season
			cashflow.date = season_to_date(year, season)
			cashflow.surrogate_key = stock_symbol + '_' + str(year) + str(season).zfill(2)
			if season == 1:
				prevSeasonData = None
			elif season == 2:
				prevSeasonData = SeasonCashflowStatement.objects.filter(symbol=stock_symbol, year=year, season__lte=1)
			elif season == 3:
				prevSeasonData = SeasonCashflowStatement.objects.filter(symbol=stock_symbol, year=year, season__lte=2)
			elif season == 4:
				prevSeasonData = SeasonCashflowStatement.objects.filter(symbol=stock_symbol, year=year, season__lte=3)
			for data in cashflows_datas:
				if data.string != None and (r'繼續營業單位稅前淨利（淨損）' in data.string or r'繼續營業單位稅前（淨利）淨損' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.profit_loss_from_continuing_operations_before_tax = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('profit_loss_from_continuing_operations_before_tax'))['sum']
				if data.string != None and r'本期稅前淨利' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.profit_loss_before_tax = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('profit_loss_before_tax'))['sum']
				if data.string != None and r'折舊費用' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.depreciation_expense = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('depreciation_expense'))['sum']
				if data.string != None and r'攤銷費用' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.amortization_expense = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('amortization_expense'))['sum']
				if data.string != None and r'利息費用' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_expense = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('interest_expense'))['sum']
				if data.string != None and r'利息收入' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_income = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('interest_income'))['sum']
				if data.string != None and r'股份基礎給付酬勞成本' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.share_based_payments = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('share_based_payments'))['sum']
				if data.string != None and (r'採用權益法認列之關聯企業及合資損失（利益）之份額' in data.string or r'採用權益法認列之關聯企業及合資（損失）利益之份額' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.share_of_profit_loss_of_associates_using_equity_method = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('share_of_profit_loss_of_associates_using_equity_method'))['sum']
				if data.string != None and (r'處分及報廢不動產、廠房及設備損失（利益）' in data.string or r'處分及報廢不動產、廠房及設備（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.loss_gain_on_disposal_of_property_plan_and_equipment = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('loss_gain_on_disposal_of_property_plan_and_equipment'))['sum']
				if data.string != None and (r'處分投資損失（利益）' in data.string or r'處分投資（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.loss_gain_on_disposal_of_investments = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('loss_gain_on_disposal_of_investments'))['sum']
				if data.string != None and (r'處分採用權益法之投資損失（利益）' in data.string or r'處分採用權益法之投資（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.loss_gain_on_disposal_of_investments_using_equity_method = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('loss_gain_on_disposal_of_investments_using_equity_method'))['sum']
				if data.string != None and r'金融資產減損損失' in data.string and r'非' not in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.impairment_loss_on_financial_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('impairment_loss_on_financial_assets'))['sum']
				if data.string != None and r'非金融資產減損損失' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.impairment_loss_on_non_financial_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('impairment_loss_on_non_financial_assets'))['sum']
				if data.string != None and (r'已實現銷貨損失（利益）' in data.string or r'已實現銷貨（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.realized_loss_profit_on_from_sales = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('realized_loss_profit_on_from_sales'))['sum']
				if data.string != None and (r'未實現外幣兌換損失（利益）' in data.string or r'未實現外幣兌換（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.unrealized_foreign_exchange_loss_gain = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('unrealized_foreign_exchange_loss_gain'))['sum']
				if data.string != None and r'其他項目' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.other_adjustments_to_reconcile_profit_loss = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('other_adjustments_to_reconcile_profit_loss'))['sum']
				if data.string != None and r'不影響現金流量之收益費損項目合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_adjustments_to_reconcile_profit_loss = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('total_adjustments_to_reconcile_profit_loss'))['sum']
				if data.string != None and (r'持有供交易之金融資產（增加）減少' in data.string or r'持有供交易之金融資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_financial_assets_held_for_trading = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_increase_in_financial_assets_held_for_trading'))['sum']
				if data.string != None and (r'避險之衍生金融資產（增加）減少' in data.string or r'避險之衍生金融資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_derivative_financial_assets_for_hedging = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_increase_in_derivative_financial_assets_for_hedging'))['sum']
				if data.string != None and (r'應收帳款（增加）減少' in data.string or r'應收帳款增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_accounts_receivable = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_increase_in_accounts_receivable'))['sum']
				if data.string != None and (r'應收帳款－關係人（增加）減少' in data.string or r'應收帳款－關係人增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_accounts_receivable_from_related_parties = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_increase_in_accounts_receivable_from_related_parties'))['sum']
				if data.string != None and (r'其他應收款－關係人（增加）減少' in data.string or r'其他應收款－關係人增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_other_receivable_due_from_related_parties = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_increase_in_other_receivable_due_from_related_parties'))['sum']
				if data.string != None and (r'存貨（增加）減少' in data.string or r'存貨增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_inventories = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_increase_in_inventories'))['sum']
				if data.string != None and (r'其他產（增加）減少' in data.string or r'其他流動資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_other_current_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_increase_in_other_current_assets'))['sum']
				if data.string != None and (r'其他金融資產（增加）減少' in data.string or r'其他金融資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_other_financial_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_increase_in_other_financial_assets'))['sum']
				if data.string != None and r'與營業活動相關之資產之淨變動合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_changes_in_operating_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('total_changes_in_operating_assets'))['sum']
				if data.string != None and (r'應付帳款增加（減少）' in data.string or r'應付帳款（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_accounts_payable = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_decrease_in_accounts_payable'))['sum']
				if data.string != None and (r'應付帳款－關係人（增加）減少' in data.string or r'應付帳款－關係人增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_accounts_payable_to_related_parties = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_decrease_in_accounts_payable_to_related_parties'))['sum']
				if data.string != None and (r'負債準備增加（減少）' in data.string or r'負債準備（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_provisions = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_decrease_in_provisions'))['sum']
				if data.string != None and (r'其他流動負債增加（減少）' in data.string or r'其他流動負債（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_other_current_liabilities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_decrease_in_other_current_liabilities'))['sum']
				if data.string != None and (r'應計退休金負債增加（減少）' in data.string or r'應計退休金負債（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_accrued_pension_liabilities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_decrease_in_accrued_pension_liabilities'))['sum']
				if data.string != None and (r'其他營業負債增加（減少）' in data.string or r'其他營業負債（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_other_operating_liabilities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_decrease_in_other_operating_liabilities'))['sum']
				if data.string != None and r'與營業活動相關之負債之淨變動合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_changes_in_operating_liabilities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('total_changes_in_operating_liabilities'))['sum']
				if data.string != None and r'與營業活動相關之資產及負債之淨變動合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_changes_in_operating_assets_and_liabilities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('total_changes_in_operating_assets_and_liabilities'))['sum']
				if data.string != None and r'調整項目合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_adjustments = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('total_adjustments'))['sum']
				if data.string != None and (r'營運產生之現金流入（流出）' in data.string or r'營運產生之現金（流入）流出' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.cash_inflow_outflow_generated_from_operations = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('cash_inflow_outflow_generated_from_operations'))['sum']
				if data.string != None and (r'退還（支付）之所得稅' in data.string or r'（退還）支付之所得稅' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.income_taxes_refund_paid = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('income_taxes_refund_paid'))['sum']
				if data.string != None and (r'營業活動之淨現金流入（流出）' in data.string or r'營業活動之淨現金（流入）流出' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.net_cash_flows_from_used_in_operating_activities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('net_cash_flows_from_used_in_operating_activities'))['sum']
				if data.string != None and r'取得備供出售金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_available_for_sale_financial_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('acquisition_of_available_for_sale_financial_assets'))['sum']
				if data.string != None and r'處分備供出售金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_available_for_sale_financial_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('proceeds_from_disposal_of_available_for_sale_financial_assets'))['sum']
				if data.string != None and r'取得持有至到期日金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_held_to_maturity_financial_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('acquisition_of_held_to_maturity_financial_assets'))['sum']
				if data.string != None and r'持有至到期日金融資產到期還本' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_repayments_of_held_to_maturity_financial_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('proceeds_from_repayments_of_held_to_maturity_financial_assets'))['sum']
				if data.string != None and r'取得以成本衡量之金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_financial_assets_at_cost = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('acquisition_of_financial_assets_at_cost'))['sum']
				if data.string != None and r'處分以成本衡量之金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_financial_assets_at_cost = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('proceeds_from_disposal_of_financial_assets_at_cost'))['sum']
				if data.string != None and r'處分採用權益法之投資' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_investments_using_equity_method = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('proceeds_from_disposal_of_investments_using_equity_method'))['sum']
				if data.string != None and r'處分子公司' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_subsidiaries = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('proceeds_from_disposal_of_subsidiaries'))['sum']
				if data.string != None and r'取得不動產、廠房及設備' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_property_plant_and_equipment = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('acquisition_of_property_plant_and_equipment'))['sum']
				if data.string != None and r'處分不動產、廠房及設備' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_property_plant_and_equipment = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('proceeds_from_disposal_of_property_plant_and_equipment'))['sum']
				if data.string != None and r'存出保證金增加' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_refundable_deposits = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_in_refundable_deposits'))['sum']
				if data.string != None and r'存出保證金減少' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_in_refundable_deposits = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_in_refundable_deposits'))['sum']
				if data.string != None and r'取得無形資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_intangible_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('acquisition_of_intangible_assets'))['sum']
				if data.string != None and (r'長期應收租賃款減少' in data.string or r'應收租賃款減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_in_long_term_lease_and_installment_receivables = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_in_long_term_lease_and_installment_receivables'))['sum']
				if data.string != None and (r'其他金融資產增加' in data.string or r'其他金融資產（增加）減少' in data.string or r'其他金融資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_other_financial_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_in_other_financial_assets'))['sum']
				if data.string != None and r'其他非流動資產增加' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_other_non_current_assets = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_in_other_non_current_assets'))['sum']
				if data.string != None and r'收取之利息' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_received = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('interest_received'))['sum']
				if data.string != None and r'收取之股利' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.dividends_received = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('dividends_received'))['sum']
				if data.string != None and r'其他投資活動' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.other_investing_activities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('other_investing_activities'))['sum']
				if data.string != None and (r'投資活動之淨現金流入（流出）' in data.string or r'投資活動之淨現金（流入）流出' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.net_cash_flows_from_used_in_investing_activities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('net_cash_flows_from_used_in_investing_activities'))['sum']
				if data.string != None and r'短期借款增加' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_short_term_loans = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_in_short_term_loans'))['sum']
				if data.string != None and r'發行公司債' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_issuing_bonds = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('proceeds_from_issuing_bonds'))['sum']
				if data.string != None and r'償還公司債' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.repayments_of_bonds = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('repayments_of_bonds'))['sum']
				if data.string != None and r'舉借長期借款' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_long_term_debt = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('proceeds_from_long_term_debt'))['sum']
				if data.string != None and r'償還長期借款' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.repayments_of_long_term_debt = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('repayments_of_long_term_debt'))['sum']
				if data.string != None and r'存入保證金增加' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_guarantee_deposits_received = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('increase_in_guarantee_deposits_received'))['sum']
				if data.string != None and r'存入保證金減少' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_in_guarantee_deposits_received = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_in_guarantee_deposits_received'))['sum']
				if data.string != None and r'應付租賃款減少' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_in_lease_payable = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('decrease_in_lease_payable'))['sum']
				if data.string != None and r'員工執行認股權' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.exercise_of_employee_share_options = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('exercise_of_employee_share_options'))['sum']
				if data.string != None and r'支付之利息' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_paid = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('interest_paid'))['sum']
				if data.string != None and r'非控制權益變動' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.change_in_non_controlling_interests = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('change_in_non_controlling_interests'))['sum']
				if data.string != None and r'其他籌資活動' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.other_financing_activities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('other_financing_activities'))['sum']
				if data.string != None and (r'籌資活動之淨現金流入（流出）' in data.string or r'籌資活動之淨現金（流入）流出' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.net_cash_flows_from_used_in_financing_activities = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('net_cash_flows_from_used_in_financing_activities'))['sum']
				if data.string != None and r'匯率變動對現金及約當現金之影響' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('effect_of_exchange_rate_changes_on_cash_and_cash_equivalents'))['sum']
				if data.string != None and (r'本期現金及約當現金增加（減少）數' in data.string or r'本期現金及約當現金（增加）減少數' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.net_increase_decrease_in_cash_and_cash_equivalents = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('net_increase_decrease_in_cash_and_cash_equivalents'))['sum']
				if data.string != None and r'期初現金及約當現金餘額' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.cash_and_cash_equivalents_at_beginning_of_period = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('cash_and_cash_equivalents_at_beginning_of_period'))['sum']
				if data.string != None and r'期末現金及約當現金餘額' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.cash_and_cash_equivalents_at_end_of_period = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('cash_and_cash_equivalents_at_end_of_period'))['sum']
				if data.string != None and r'資產負債表帳列之現金及約當現金' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.cash_and_cash_equivalents_in_the_statement_of_financial_position = st_to_decimal(next_data.string) if (prevSeasonData is None or prevSeasonData.count() == 0) else st_to_decimal(next_data.string) - prevSeasonData.aggregate(sum=Sum('cash_and_cash_equivalents_in_the_statement_of_financial_position'))['sum']
				cashflow.free_cash_flow = cashflow.net_cash_flows_from_used_in_operating_activities + cashflow.net_cash_flows_from_used_in_investing_activities
				if data.string != None and r'利息收入' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_income = st_to_decimal(next_data.string)
			response.close()
			if cashflow.profit_loss_from_continuing_operations_before_tax:
				cashflow.data_date = financial_date_to_data_date(year, season)
				cashflow.save()
	cnt = SeasonCashflowStatement.objects.filter(year=year, season=season).count()
	lastDate = SeasonCashflowStatement.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = SeasonCashflowStatement.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='sbs', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " sbs in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(season)})

	return HttpResponse(json_obj, content_type="application/json")

def old_update_season_financial_ratio(request):
	print ('start update season financial ratio')
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
	sisSymbol = SeasonIncomeStatement.objects.filter(year=year, season=season).values_list('symbol', flat=True)
	sbsSymbol = SeasonBalanceSheet.objects.filter(year=year, season=season).values_list('symbol', flat=True)
	scfSymbol = SeasonCashflowStatement.objects.filter(year=year, season=season).values_list('symbol', flat=True)
	union = set(sisSymbol).union(set(sbsSymbol)).union(set(scfSymbol))
	intersection = set(sisSymbol).intersection(set(sbsSymbol)).intersection(set(scfSymbol))
	diff = union.difference(intersection)
	print (diff)
	for stockID in intersection:
		has_sbs_prev = False
		try:
			sis = SeasonIncomeStatement.objects.get(year=year, season=season, symbol=stockID)
			sbs = SeasonBalanceSheet.objects.get(year=year, season=season, symbol=stockID)
			scf = SeasonCashflowStatement.objects.get(year=year, season=season, symbol=stockID)
		except:
			print ("load " + stockID + "'s data error")
			continue
		prevSeasonYear, prevSeasonSeason = prev_season(year, season)
		if SeasonBalanceSheet.objects.filter(year=prevSeasonYear, season=prevSeasonSeason, symbol=stockID):
			has_sbs_prev = True
			prev_sbs = SeasonBalanceSheet.objects.get(year=prevSeasonYear, season=prevSeasonSeason, symbol=stockID)
		ratio = SeasonFinancialRatio()
		ratio.year = year
		ratio.season = season
		ratio.symbol = stockID
		ratio.date = season_to_date(year, season)
		ratio.surrogate_key = stockID + '_' + str(year) + str(season).zfill(2)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0 and sbs.number_of_shares_in_entity_held_by_entity and sbs.number_of_shares_in_entity_held_by_entity > 0:
			total_stock = sbs.total_capital_stock - sbs.number_of_shares_in_entity_held_by_entity / 100
			if total_stock == 0:
				total_stock = sbs.total_capital_stock
		elif sbs.total_capital_stock and sbs.total_capital_stock > 0:
			total_stock = sbs.total_capital_stock
		# 毛利率 = 營業毛利（毛損）淨額 / 營業收入合計（單位：％）
		if sis.total_operating_revenue and sis.total_operating_revenue > 0:
			if sis.gross_profit_loss_from_operations:
				ratio.gross_profit_margin = sis.gross_profit_loss_from_operations / sis.total_operating_revenue * 100
			# 有的公司使用舊式報表，沒有營業毛利這一項，就改用繼續營業單位稅前淨利代替
			elif sis.profit_loss_from_continuing_operations_before_tax:
				ratio.gross_profit_margin = sis.profit_loss_from_continuing_operations_before_tax / sis.total_operating_revenue * 100
			else:
				pdb.set_trace()
		elif sis.total_operating_revenue and sis.total_operating_revenue == 0:
			pdb.set_trace()
			ratio.gross_profit_margin = 0
		# 營業利益率 = 營業利益（損失） / 營業收入合計（單位：％）
		if sis.total_operating_revenue and sis.total_operating_revenue > 0:
			if sis.net_operating_income_loss:
				ratio.operating_profit_margin = sis.net_operating_income_loss / sis.total_operating_revenue * 100
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
			elif sis.profit_loss_from_continuing_operations:
				ratio.operating_profit_margin = sis.profit_loss_from_continuing_operations / sis.total_operating_revenue * 100
			else:
				pdb.set_trace()
		elif sis.total_operating_revenue and sis.total_operating_revenue == 0:
			pdb.set_trace()
			ratio.operating_profit_margin = 0
		# 稅前淨利率 = 稅前純益 / 營業收入
		if sis.total_operating_revenue and sis.total_operating_revenue > 0:
			if sis.profit_loss_from_continuing_operations_before_tax:
				ratio.net_profit_margin_before_tax = sis.profit_loss_from_continuing_operations_before_tax / sis.total_operating_revenue * 100
			elif sis.profit_loss_from_continuing_operations:
				ratio.net_profit_margin_before_tax = sis.profit_loss_from_continuing_operations / sis.total_operating_revenue * 100
		elif sis.total_operating_revenue and sis.total_operating_revenue == 0:
			ratio.net_profit_margin_before_tax = 0
		# 稅後淨利率 = 稅後純益 / 營業收入
		if sis.total_operating_revenue and sis.total_operating_revenue > 0:
			if sis.profit_loss:
				ratio.net_profit_margin = sis.profit_loss / sis.total_operating_revenue * 100
		elif sis.total_operating_revenue and sis.total_operating_revenue == 0:
			ratio.net_profit_margin = 0
		# 每股淨值(元)
		#net_value_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
		# 每股營業額(元)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0:
			if sis.total_operating_revenue:
				ratio.revenue_per_share = sis.total_operating_revenue / total_stock * 10
		elif sbs.total_capital_stock and sbs.total_capital_stock == 0:
			ratio.revenue_per_share = 0
		# 每股營業利益(元)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0:
			if sis.net_operating_income_loss:
				ratio.operating_profit_per_share = sis.net_operating_income_loss / total_stock * 10
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替	
			elif sis.profit_loss_from_continuing_operations:
				ratio.operating_profit_per_share = sis.profit_loss_from_continuing_operations / total_stock * 10
		elif sbs.total_capital_stock and sbs.total_capital_stock == 0:
			ratio.operating_profit_per_share = 0
		# 每股稅前淨利(元)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0:
			if sis.profit_loss_from_continuing_operations_before_tax:
				ratio.net_before_tax_profit_per_share = sis.profit_loss_from_continuing_operations_before_tax / total_stock * 10
			elif sis.profit_loss_from_continuing_operations:
				ratio.net_before_tax_profit_per_share = sis.profit_loss_from_continuing_operations / total_stock
		elif sbs.total_capital_stock and sbs.total_capital_stock == 0:
			ratio.net_before_tax_profit_per_share = 0
		# 每股盈餘(EPS)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0:
			if sis.profit_loss:
				ratio.earnings_per_share = sis.profit_loss / total_stock * 10
				ratio.earnings_per_share = sis.total_basic_earnings_per_share
		elif sbs.total_capital_stock and sbs.total_capital_stock == 0:
			ratio.earnings_per_share = 0
			ratio.earnings_per_share = sis.total_basic_earnings_per_share
		# 總資產報酬率(ROA) = 本期淨利（淨損） / 期初期末平均之資產總額（單位：％）
		if sis.profit_loss:
			if scf.interest_expense:
				profitLoss = sis.profit_loss + scf.interest_expense
			else:
				profitLoss = sis.profit_loss
			if has_sbs_prev:
				if sbs.total_assets and prev_sbs.total_assets:
					ratio.return_on_assets = profitLoss / ((sbs.total_assets + prev_sbs.total_assets) / 2) * 100
				elif sbs.total_assets:
					ratio.return_on_assets = profitLoss / (sbs.total_assets / 2) * 100
				else:
					ratio.return_on_assets = 0
			elif sbs.total_assets:
				ratio.return_on_assets = profitLoss / (sbs.total_assets / 2) * 100
			else:
				ratio.return_on_assets = 0
		# 股東權益報酬率(ROE) = 本期淨利(稅前) / 期初期末平均之權益總額(期初股東權益+期末股東權益/2)
		if sis.profit_loss:
			if has_sbs_prev:
				if sbs.total_equity and prev_sbs.total_equity:
					ratio.return_on_equity = sis.profit_loss / ((sbs.total_equity + prev_sbs.total_equity) / 2) * 100
				elif sbs.total_equity:
					ratio.return_on_equity = sis.profit_loss / (sbs.total_equity / 2) * 100
				else:
					ratio.return_on_equity = 0
			elif sbs.total_equity:
					ratio.return_on_equity = sis.profit_loss / (sbs.total_equity / 2) * 100
			else:
				ratio.return_on_equity = 0
		# ---償債能力---
		# 流動比率 = 流動資產合計 / 流動負債合計
		if sbs.total_current_liabilities and sbs.total_current_liabilities != 0:
			if sbs.total_current_assets:
				ratio.current_ratio = sbs.total_current_assets / sbs.total_current_liabilities * 100
		# 速動比率 = 速動資產合計 / 流動負債合計（速動資產 = 流動資產 - 存貨 - 預付款項 - 其他流動資產）
		if sbs.total_current_liabilities and sbs.total_current_liabilities != 0:
			numerator = Decimal(0)
			if sbs.total_current_assets:
				numerator += sbs.total_current_assets
			if sbs.total_inventories:
				numerator -= sbs.total_inventories
			if sbs.total_prepayments:
				numerator -= sbs.total_prepayments
			if sbs.total_other_current_assets:
				numerator -= sbs.total_other_current_assets
			ratio.quick_ratio = numerator / sbs.total_current_liabilities * 100
		#?? 金融負債比率 = 金融負債總額 / 資產總額（金融負債 = 短期借款 + 應付短期票券 + 應付公司債 + 長期借款，要付息的，單位：％）
		#未完成
		if sbs.total_assets and sbs.total_assets != 0:
			numerator = Decimal(0)
			if sbs.total_short_term_borrowings:
				numerator += sbs.total_short_term_borrowings
			if sbs.short_term_notes_and_bills_payable:
				numerator += sbs.short_term_notes_and_bills_payable
			if sbs.total_bonds_payable:
				numerator += sbs.total_bonds_payable
			if sbs.total_long_term_borrowings:
				numerator += sbs.total_long_term_borrowings
			ratio.financial_debt_ratio = numerator / sbs.total_assets * 100
		# 負債比率
		if sbs.total_assets and sbs.total_assets != 0:
			if sbs.total_liabilities:
				ratio.debt_ratio = sbs.total_liabilities / sbs.total_assets * 100
		# 利息保障倍數
		if scf.interest_expense and scf.interest_expense != 0:
			if sis.profit_loss_from_continuing_operations_before_tax:
				ratio.interest_cover = (scf.interest_expense + sis.profit_loss_from_continuing_operations_before_tax) / scf.interest_expense
		# ---經營能力---
		# 應收帳款週轉率 = 營業收入合計 / 期初期末平均之應收票據淨額+應收帳款淨額+應收帳款－關係人淨額（單位：次／季）
		if sis.total_operating_revenue and sis.total_operating_revenue != 0:
			numerator = sis.total_operating_revenue
			denumerator = Decimal(0)
			if sbs.notes_receivable:
				denumerator += sbs.notes_receivable
			if sbs.accounts_receivable:
				denumerator += sbs.accounts_receivable
			if sbs.accounts_receivable_due_from_related_parties:
				denumerator += sbs.accounts_receivable_due_from_related_parties
			if has_sbs_prev:
				if prev_sbs.notes_receivable:
					denumerator += prev_sbs.notes_receivable
				if prev_sbs.accounts_receivable:
					denumerator += prev_sbs.accounts_receivable
				if prev_sbs.accounts_receivable_due_from_related_parties:
					denumerator += prev_sbs.accounts_receivable_due_from_related_parties
				denumerator /= 2
			if denumerator == 0:
				ratio.accounts_receivable_turnover_ratio = 0
			else:
				ratio.accounts_receivable_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.accounts_receivable_turnover_ratio = 0
		# 存貨週轉率 = 營業成本合計 / 期初期末平均之存貨（單位：次／季）
		if sis.total_operating_costs and sis.total_operating_costs != 0:
			numerator = sis.total_operating_costs
			denumerator = Decimal(0)
			if sbs.total_inventories:
				denumerator += sbs.total_inventories
			if has_sbs_prev:
				if prev_sbs.total_inventories:
					denumerator += prev_sbs.total_inventories
				denumerator /= 2
			if denumerator == 0:
				ratio.inventory_turnover_ratio = 0
			else:
				ratio.inventory_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.inventory_turnover_ratio = 0
		# 固定資產週轉率 = 營業收入合計 / 期初期末平均之不動產、廠房及設備（單位：次／季）
		if sis.total_operating_costs and sis.total_operating_costs != 0:
			numerator = sis.total_operating_costs
			denumerator = Decimal(0)
			if sbs.total_property_plant_and_equipment:
				denumerator += sbs.total_property_plant_and_equipment
			if has_sbs_prev:
				if prev_sbs.total_property_plant_and_equipment:
					denumerator += prev_sbs.total_property_plant_and_equipment
				denumerator /= 2
			if denumerator == 0:
				ratio.fixed_asset_turnover_ratio = 0
			else:
				ratio.fixed_asset_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.fixed_asset_turnover_ratio = 0
		# 總資產週轉率 = 營業收入合計 / 期初期末平均之資產總額（單位：次／季）
		if sis.total_operating_revenue and sis.total_operating_revenue != 0:
			numerator = sis.total_operating_revenue
			denumerator = Decimal(0)
			if sbs.total_assets:
				denumerator += sbs.total_assets
			if has_sbs_prev:
				if prev_sbs.total_assets:
					denumerator += prev_sbs.total_assets
				denumerator /= 2
			if denumerator == 0:
				ratio.total_asset_turnover_ratio = 0
			else:
				ratio.total_asset_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.total_asset_turnover_ratio = 0
		# ---黃國華指標---
		# 存貨營收比 = 存貨 / 營業收入合計（評估存貨要多少季可以消化完畢，單位：季）
		if sis.total_operating_revenue and sis.total_operating_revenue != 0:
			if sbs.total_inventories:
				ratio.inventory_sales_ratio = sbs.total_inventories / sis.total_operating_revenue
			else:
				ratio.inventory_sales_ratio = 0
		else:
			ratio.inventory_sales_ratio = 0
		# 備供出售比率 = 備供出售金融資產－非流動淨額 / 權益總額（單位：％）
		if sbs.total_equity and sbs.total_equity != 0:
			if sbs.non_current_available_for_sale_financial_assets:
				ratio.available_for_sale_to_equity_ratio = sbs.non_current_available_for_sale_financial_assets / sbs.total_equity * 100
			else:
				ratio.available_for_sale_to_equity_ratio = 0
		else:
			ratio.available_for_sale_to_equity_ratio = 0
		# 無形資產比率 = 無形資產 / 權益總額（單位：％）
		if sbs.total_equity and sbs.total_equity != 0:
			if sbs.intangible_assets:
				ratio.intangible_asset_to_equity_ratio = sbs.intangible_assets / sbs.total_equity * 100
			else:
				ratio.intangible_asset_to_equity_ratio = 0
		else:
			ratio.intangible_asset_to_equity_ratio = 0
		# 折舊負擔比率 = 折舊費用 / 營業收入合計（評估營收必須拿多少來攤提折舊，單位：％）
		if sis.total_operating_revenue and sis.total_operating_revenue != 0:
			if scf.depreciation_expense:
				ratio.depreciation_to_sales_ratio = scf.depreciation_expense / sis.total_operating_revenue
			else:
				ratio.depreciation_to_sales_ratio = 1000
		else:
			ratio.depreciation_to_sales_ratio = 1000
		# 營業利益佔稅前淨利比率 = 營業利益（損失） / 稅前淨利（淨損）（單位：％）
		if sis.profit_loss_from_continuing_operations_before_tax and sis.profit_loss_from_continuing_operations_before_tax != 0:
			numerator = Decimal(0)
			if sis.net_operating_income_loss:
				numerator += sis.net_operating_income_loss
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
			elif sis.profit_loss_from_continuing_operations_before_tax:
				numerator += sis.profit_loss_from_continuing_operations_before_tax
			ratio.operating_profit_to_net_profit_before_tax_ratio = numerator / sis.profit_loss_from_continuing_operations_before_tax
		# 現金股息配發率(季資料忽略此項目)
		# 營業稅率
		if sis.profit_loss_from_continuing_operations_before_tax and sis.profit_loss_from_continuing_operations_before_tax != 0:
			if sis.total_tax_expense:
				if sis.profit_loss_from_continuing_operations_before_tax < 0:
					ratio.tax_rate = -sis.total_tax_expense / sis.profit_loss_from_continuing_operations_before_tax
				else:
					ratio.tax_rate = sis.total_tax_expense / sis.profit_loss_from_continuing_operations_before_tax
			else:
				ratio.tax_rate = 0
		ratio.save()
		# print (ratio.symbol + " season financial ratio saved")
	cnt = SeasonFinancialRatio.objects.filter(year=year, season=season).count()
	lastDate = SeasonFinancialRatio.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = SeasonFinancialRatio.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name = "sfr", last_update_date = datetime.date.today(), 
										last_data_date = lastDate, notes="There is " + str(lastDateDataCnt) + " datas")
	updateManagement.save()
	json_obj = json.dumps({"updateDate": updateManagement.last_update_date.strftime("%y-%m-%d"),
							"dataDate": lastDate.strftime("%y-%m-%d"), "notes": "Update " + str(cnt) + " season cashflow statements on " + str(year) + "-" + str(season)})
	return HttpResponse(json_obj, content_type="application/json")

def update_season_financial_ratio(request):
	print ('start update season financial ratio')
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
	sisSymbol = SeasonIncomeStatement.objects.filter(year=year, season=season).values_list('symbol', flat=True)
	sbsSymbol = SeasonBalanceSheet.objects.filter(year=year, season=season).values_list('symbol', flat=True)
	scfSymbol = SeasonCashflowStatement.objects.filter(year=year, season=season).values_list('symbol', flat=True)
	union = set(sisSymbol).union(set(sbsSymbol)).union(set(scfSymbol))
	intersection = set(sisSymbol).intersection(set(sbsSymbol)).intersection(set(scfSymbol))
	diff = union.difference(intersection)
	print (diff)
	for stockID in intersection:
		has_sbs_prev = False
		try:
			sis = SeasonIncomeStatement.objects.get(year=year, season=season, symbol=stockID)
			sbs = SeasonBalanceSheet.objects.get(year=year, season=season, symbol=stockID)
			scf = SeasonCashflowStatement.objects.get(year=year, season=season, symbol=stockID)
		except:
			print ("load " + stockID + "'s data error")
			continue
		prevSeasonYear, prevSeasonSeason = prev_season(year, season)
		if SeasonBalanceSheet.objects.filter(year=prevSeasonYear, season=prevSeasonSeason, symbol=stockID):
			has_sbs_prev = True
			prev_sbs = SeasonBalanceSheet.objects.get(year=prevSeasonYear, season=prevSeasonSeason, symbol=stockID)
		ratio = SeasonFinancialRatio()
		ratio.year = year
		ratio.season = season
		ratio.symbol = stockID
		ratio.date = season_to_date(year, season)
		ratio.surrogate_key = stockID + '_' + str(year) + str(season).zfill(2)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0 and sbs.number_of_shares_in_entity_held_by_entity and sbs.number_of_shares_in_entity_held_by_entity > 0:
			total_stock = sbs.total_capital_stock - sbs.number_of_shares_in_entity_held_by_entity / 100
			if total_stock == 0:
				total_stock = sbs.total_capital_stock
		elif sbs.total_capital_stock and sbs.total_capital_stock > 0:
			total_stock = sbs.total_capital_stock
		# 毛利率 = 營業毛利（毛損）淨額 / 營業收入合計（單位：％）
		if sis.total_operating_revenue and sis.total_operating_revenue > 0:
			if sis.gross_profit_loss_from_operations:
				ratio.gross_profit_margin = sis.gross_profit_loss_from_operations / sis.total_operating_revenue * 100
			# 有的公司使用舊式報表，沒有營業毛利這一項，就改用繼續營業單位稅前淨利代替
			elif sis.profit_loss_from_continuing_operations:
				ratio.gross_profit_margin = sis.profit_loss_from_continuing_operations / sis.total_operating_revenue * 100
		elif sis.total_operating_revenue and sis.total_operating_revenue == 0:
			ratio.gross_profit_margin = 0
		# 營業利益率 = 營業利益（損失） / 營業收入合計（單位：％）
		if sis.total_operating_revenue and sis.total_operating_revenue > 0:
			if sis.net_operating_income_loss:
				ratio.operating_profit_margin = sis.net_operating_income_loss / sis.total_operating_revenue * 100
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
			elif sis.profit_loss_from_continuing_operations:
				ratio.operating_profit_margin = sis.profit_loss_from_continuing_operations / sis.total_operating_revenue * 100
		elif sis.total_operating_revenue and sis.total_operating_revenue == 0:
			ratio.operating_profit_margin = 0
		# 稅前淨利率 = 稅前純益 / 營業收入
		if sis.total_operating_revenue and sis.total_operating_revenue > 0:
			if sis.profit_loss_from_continuing_operations_before_tax:
				ratio.net_profit_margin_before_tax = sis.profit_loss_from_continuing_operations_before_tax / sis.total_operating_revenue * 100
			elif sis.profit_loss_from_continuing_operations:
				ratio.net_profit_margin_before_tax = sis.profit_loss_from_continuing_operations / sis.total_operating_revenue * 100
		elif sis.total_operating_revenue and sis.total_operating_revenue == 0:
			ratio.net_profit_margin_before_tax = 0
		# 稅後淨利率 = 稅後純益 / 營業收入
		if sis.total_operating_revenue and sis.total_operating_revenue > 0:
			if sis.profit_loss:
				ratio.net_profit_margin = sis.profit_loss / sis.total_operating_revenue * 100
		elif sis.total_operating_revenue and sis.total_operating_revenue == 0:
			ratio.net_profit_margin = 0
		# 每股淨值(元)
		#net_value_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
		# 每股營業額(元)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0:
			if sis.total_operating_revenue:
				ratio.revenue_per_share = sis.total_operating_revenue / total_stock * 10
		elif sbs.total_capital_stock and sbs.total_capital_stock == 0:
			ratio.revenue_per_share = 0
		# 每股營業利益(元)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0:
			if sis.net_operating_income_loss:
				ratio.operating_profit_per_share = sis.net_operating_income_loss / total_stock * 10
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
			elif sis.profit_loss_from_continuing_operations:
				ratio.operating_profit_per_share = sis.profit_loss_from_continuing_operations / total_stock * 10
		elif sbs.total_capital_stock and sbs.total_capital_stock == 0:
			ratio.operating_profit_per_share = 0
		# 每股稅前淨利(元)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0:
			if sis.profit_loss_from_continuing_operations_before_tax:
				ratio.net_before_tax_profit_per_share = sis.profit_loss_from_continuing_operations_before_tax / total_stock * 10
			elif sis.profit_loss_from_continuing_operations:
				ratio.net_before_tax_profit_per_share = sis.profit_loss_from_continuing_operations / total_stock
		elif sbs.total_capital_stock and sbs.total_capital_stock == 0:
			ratio.net_before_tax_profit_per_share = 0
		# 每股盈餘(EPS)
		if sbs.total_capital_stock and sbs.total_capital_stock > 0:
			if sis.profit_loss:
				ratio.earnings_per_share = sis.profit_loss / total_stock * 10
				ratio.earnings_per_share = sis.total_basic_earnings_per_share
		elif sbs.total_capital_stock and sbs.total_capital_stock == 0:
			ratio.earnings_per_share = 0
			ratio.earnings_per_share = sis.total_basic_earnings_per_share
		# 總資產報酬率(ROA) = 本期淨利（淨損） / 期初期末平均之資產總額（單位：％）
		if sis.profit_loss:
			if scf.interest_expense:
				profitLoss = sis.profit_loss + scf.interest_expense
			else:
				profitLoss = sis.profit_loss
			if has_sbs_prev:
				if sbs.total_assets and prev_sbs.total_assets:
					ratio.return_on_assets = profitLoss / ((sbs.total_assets + prev_sbs.total_assets) / 2) * 100
				elif sbs.total_assets:
					ratio.return_on_assets = profitLoss / (sbs.total_assets / 2) * 100
				else:
					ratio.return_on_assets = 0
			elif sbs.total_assets:
				ratio.return_on_assets = profitLoss / (sbs.total_assets / 2) * 100
			else:
				ratio.return_on_assets = 0
		# 股東權益報酬率(ROE) = 本期淨利(稅前) / 期初期末平均之權益總額(期初股東權益+期末股東權益/2)
		if sis.profit_loss:
			if has_sbs_prev:
				if sbs.total_equity and prev_sbs.total_equity:
					ratio.return_on_equity = sis.profit_loss / ((sbs.total_equity + prev_sbs.total_equity) / 2) * 100
				elif sbs.total_equity:
					ratio.return_on_equity = sis.profit_loss / (sbs.total_equity / 2) * 100
				else:
					ratio.return_on_equity = 0
			elif sbs.total_equity:
					ratio.return_on_equity = sis.profit_loss / (sbs.total_equity / 2) * 100
			else:
				ratio.return_on_equity = 0
		# ---償債能力---
		# 流動比率 = 流動資產合計 / 流動負債合計
		if sbs.total_current_liabilities and sbs.total_current_liabilities != 0:
			if sbs.total_current_assets:
				ratio.current_ratio = sbs.total_current_assets / sbs.total_current_liabilities * 100
		# 速動比率 = 速動資產合計 / 流動負債合計（速動資產 = 流動資產 - 存貨 - 預付款項 - 其他流動資產）
		if sbs.total_current_liabilities and sbs.total_current_liabilities != 0:
			numerator = Decimal(0)
			if sbs.total_current_assets:
				numerator += sbs.total_current_assets
			if sbs.total_inventories:
				numerator -= sbs.total_inventories
			if sbs.total_prepayments:
				numerator -= sbs.total_prepayments
			if sbs.total_other_current_assets:
				numerator -= sbs.total_other_current_assets
			ratio.quick_ratio = numerator / sbs.total_current_liabilities * 100
		#?? 金融負債比率 = 金融負債總額 / 資產總額（金融負債 = 短期借款 + 應付短期票券 + 應付公司債 + 長期借款，要付息的，單位：％）
		#未完成
		if sbs.total_assets and sbs.total_assets != 0:
			numerator = Decimal(0)
			if sbs.total_short_term_borrowings:
				numerator += sbs.total_short_term_borrowings
			if sbs.short_term_notes_and_bills_payable:
				numerator += sbs.short_term_notes_and_bills_payable
			if sbs.total_bonds_payable:
				numerator += sbs.total_bonds_payable
			if sbs.total_long_term_borrowings:
				numerator += sbs.total_long_term_borrowings
			ratio.financial_debt_ratio = numerator / sbs.total_assets * 100
		# 負債比率
		if sbs.total_assets and sbs.total_assets != 0:
			if sbs.total_liabilities:
				ratio.debt_ratio = sbs.total_liabilities / sbs.total_assets * 100
		# 利息保障倍數
		if scf.interest_expense and scf.interest_expense != 0:
			if sis.profit_loss_from_continuing_operations_before_tax:
				ratio.interest_cover = (scf.interest_expense + sis.profit_loss_from_continuing_operations_before_tax) / scf.interest_expense
		# ---經營能力---
		# 應收帳款週轉率 = 營業收入合計 / 期初期末平均之應收票據淨額+應收帳款淨額+應收帳款－關係人淨額（單位：次／季）
		if sis.total_operating_revenue and sis.total_operating_revenue != 0:
			numerator = sis.total_operating_revenue
			denumerator = Decimal(0)
			if sbs.notes_receivable:
				denumerator += sbs.notes_receivable
			if sbs.accounts_receivable:
				denumerator += sbs.accounts_receivable
			if sbs.accounts_receivable_due_from_related_parties:
				denumerator += sbs.accounts_receivable_due_from_related_parties
			if has_sbs_prev:
				if prev_sbs.notes_receivable:
					denumerator += prev_sbs.notes_receivable
				if prev_sbs.accounts_receivable:
					denumerator += prev_sbs.accounts_receivable
				if prev_sbs.accounts_receivable_due_from_related_parties:
					denumerator += prev_sbs.accounts_receivable_due_from_related_parties
				denumerator /= 2
			if denumerator == 0:
				ratio.accounts_receivable_turnover_ratio = 0
			else:
				ratio.accounts_receivable_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.accounts_receivable_turnover_ratio = 0
		# 存貨週轉率 = 營業成本合計 / 期初期末平均之存貨（單位：次／季）
		if sis.total_operating_cost and sis.total_operating_cost != 0:
			numerator = sis.total_operating_cost
			denumerator = Decimal(0)
			if sbs.total_inventories:
				denumerator += sbs.total_inventories
			if has_sbs_prev:
				if prev_sbs.total_inventories:
					denumerator += prev_sbs.total_inventories
				denumerator /= 2
			if denumerator == 0:
				ratio.inventory_turnover_ratio = 0
			else:
				ratio.inventory_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.inventory_turnover_ratio = 0
		# 固定資產週轉率 = 營業收入合計 / 期初期末平均之不動產、廠房及設備（單位：次／季）
		if sis.total_operating_cost and sis.total_operating_cost != 0:
			numerator = sis.total_operating_cost
			denumerator = Decimal(0)
			if sbs.total_property_plant_and_equipment:
				denumerator += sbs.total_property_plant_and_equipment
			if has_sbs_prev:
				if prev_sbs.total_property_plant_and_equipment:
					denumerator += prev_sbs.total_property_plant_and_equipment
				denumerator /= 2
			if denumerator == 0:
				ratio.fixed_asset_turnover_ratio = 0
			else:
				ratio.fixed_asset_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.fixed_asset_turnover_ratio = 0
		# 總資產週轉率 = 營業收入合計 / 期初期末平均之資產總額（單位：次／季）
		if sis.total_operating_revenue and sis.total_operating_revenue != 0:
			numerator = sis.total_operating_revenue
			denumerator = Decimal(0)
			if sbs.total_assets:
				denumerator += sbs.total_assets
			if has_sbs_prev:
				if prev_sbs.total_assets:
					denumerator += prev_sbs.total_assets
				denumerator /= 2
			if denumerator == 0:
				ratio.total_asset_turnover_ratio = 0
			else:
				ratio.total_asset_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.total_asset_turnover_ratio = 0
		# ---黃國華指標---
		# 存貨營收比 = 存貨 / 營業收入合計（評估存貨要多少季可以消化完畢，單位：季）
		if sis.total_operating_revenue and sis.total_operating_revenue != 0:
			if sbs.total_inventories:
				ratio.inventory_sales_ratio = sbs.total_inventories / sis.total_operating_revenue
			else:
				ratio.inventory_sales_ratio = 0
		else:
			ratio.inventory_sales_ratio = 0
		# 備供出售比率 = 備供出售金融資產－非流動淨額 / 權益總額（單位：％）
		if sbs.total_equity and sbs.total_equity != 0:
			if sbs.non_current_available_for_sale_financial_assets:
				ratio.available_for_sale_to_equity_ratio = sbs.non_current_available_for_sale_financial_assets / sbs.total_equity * 100
			else:
				ratio.available_for_sale_to_equity_ratio = 0
		else:
			ratio.available_for_sale_to_equity_ratio = 0
		# 無形資產比率 = 無形資產 / 權益總額（單位：％）
		if sbs.total_equity and sbs.total_equity != 0:
			if sbs.intangible_assets:
				ratio.intangible_asset_to_equity_ratio = sbs.intangible_assets / sbs.total_equity * 100
			else:
				ratio.intangible_asset_to_equity_ratio = 0
		else:
			ratio.intangible_asset_to_equity_ratio = 0
		# 折舊負擔比率 = 折舊費用 / 營業收入合計（評估營收必須拿多少來攤提折舊，單位：％）
		if sis.total_operating_revenue and sis.total_operating_revenue != 0:
			if scf.depreciation_expense:
				ratio.depreciation_to_sales_ratio = scf.depreciation_expense / sis.total_operating_revenue
			else:
				ratio.depreciation_to_sales_ratio = 1000
		else:
			ratio.depreciation_to_sales_ratio = 1000
		# 營業利益佔稅前淨利比率 = 營業利益（損失） / 稅前淨利（淨損）（單位：％）
		if sis.profit_loss_from_continuing_operations_before_tax and sis.profit_loss_from_continuing_operations_before_tax != 0:
			numerator = Decimal(0)
			if sis.net_operating_income_loss:
				numerator += sis.net_operating_income_loss
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
			elif sis.profit_loss_from_continuing_operations_before_tax:
				numerator += sis.profit_loss_from_continuing_operations_before_tax
			ratio.operating_profit_to_net_profit_before_tax_ratio = numerator / sis.profit_loss_from_continuing_operations_before_tax
		# 現金股息配發率(季資料忽略此項目)
		# 營業稅率
		if sis.profit_loss_from_continuing_operations_before_tax and sis.profit_loss_from_continuing_operations_before_tax != 0:
			if sis.total_tax_expense:
				if sis.profit_loss_from_continuing_operations_before_tax < 0:
					ratio.tax_rate = -sis.total_tax_expense / sis.profit_loss_from_continuing_operations_before_tax
				else:
					ratio.tax_rate = sis.total_tax_expense / sis.profit_loss_from_continuing_operations_before_tax
			else:
				ratio.tax_rate = 0
		ratio.data_date = financial_date_to_data_date(year, season)
		ratio.save()
		# print (ratio.symbol + " season financial ratio saved")
	cnt = SeasonFinancialRatio.objects.filter(year=year, season=season).count()
	lastDate = SeasonFinancialRatio.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = SeasonFinancialRatio.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='sfr', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " sfr in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(season)})

	return HttpResponse(json_obj, content_type="application/json")

def update_year_income_statement(request):
	print ('start update year income statement')
	if 'date' in request.GET:
		date = request.GET['date']
		if date != '':
			try:
				year = int(date)
			except:
				return HttpResponse('please input correct date "year"')
		else:
			return HttpResponse('please input correct date "year"')
	else:
		return HttpResponse('please input correct date "year"')
	stockIDs = get_updated_id(year, 4)
	update_cnt = 0
	for stockID in stockIDs:
		update_cnt = update_cnt + 1
		stock_symbol = stockID
		if not (YearIncomeStatement.objects.filter(symbol=stock_symbol, year=year)):
			url = 'http://mops.twse.com.tw/mops/web/ajax_t164sb04'
			values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'sii', 'step' : '2',
					'year' : str(year-1911), 'season' : '04', 'co_id' : stock_symbol, 'firstin' : '1'}
			url_data = urllib.parse.urlencode(values).encode('utf-8')
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib.request.Request(url, url_data, headers)
			try:
				response = urllib.request.urlopen(req)
				soup = BeautifulSoup(response,from_encoding="utf-8")
				season_income_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
				busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
			except urllib.error.URLError as e:
				time.sleep(20)
				busy_msg = True
				if hasattr(e, 'reason'):
					print(stock_symbol + ' not update. Reason:', e.reason)
			# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
			while busy_msg:
				response.close()
				headers = {'User-Agent': 'Mozilla/5.0'}
				req = urllib.request.Request(url, url_data, headers)
				try:
					response = urllib.request.urlopen(req)
					soup = BeautifulSoup(response,from_encoding="utf-8")
					season_income_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
					busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
				except urllib.error.URLError as e:
					busy_msg = True
					if hasattr(e, 'reason'):
						print(stock_symbol + ' not update. Reason:', e.reason)
				if busy_msg:
					print (stock_symbol + 'time sleep') 
					time.sleep(20)
			income_statement = YearIncomeStatement()
			income_statement.symbol = stock_symbol
			income_statement.year = year
			income_statement.surrogate_key = stock_symbol + '_' + str(year)
			income_statement.date = year_to_date(year)
			owners_of_parent = 0
			print (stock_symbol + ' loaded')
			for data in season_income_datas:
				if r'營業收入合計' in data.string or r'收入合計' == data.string or r'淨收益' == data.string or r'收益合計' == data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_operating_revenue = st_to_decimal(next_data.string)
				elif r'營業成本合計' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_operating_cost = st_to_decimal(next_data.string)
				elif r'營業毛利（毛損）' == data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.gross_profit_loss_from_operations = st_to_decimal(next_data.string)
				elif r'未實現銷貨（損）益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.unrealized_profit_loss_from_sales = st_to_decimal(next_data.string)
				elif r'已實現銷貨（損）益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.realized_profit_loss_from_sales = st_to_decimal(next_data.string)
				elif r'營業毛利（毛損）淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_gross_profit_from_operations = st_to_decimal(next_data.string)
				elif r'推銷費用' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_selling_expenses = st_to_decimal(next_data.string)
				elif r'管理費用' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.administrative_expenses = st_to_decimal(next_data.string)
				elif r'研究發展費用' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.research_and_development_expenses = st_to_decimal(next_data.string)
				elif r'營業費用合計' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_operating_expenses = st_to_decimal(next_data.string)
				elif r'其他收益及費損淨額' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						income_statement.net_other_income_expenses = st_to_decimal(next_data.string)
				elif r'營業利益（損失）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_operating_income_loss = st_to_decimal(next_data.string)
				elif r'其他收入' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.other_income = st_to_decimal(next_data.string)
				elif r'其他利益及損失淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.other_gains_and_losses = st_to_decimal(next_data.string)
				elif r'財務成本淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_finance_costs = st_to_decimal(next_data.string)
				elif r'採用權益法認列之關聯企業及合資損益之份額淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.share_of_profit_loss_of_associates_using_equity_method = st_to_decimal(next_data.string)
				elif r'營業外收入及支出合計' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_non_operating_income_and_expenses = st_to_decimal(next_data.string)
				elif r'稅前淨利（淨損）' in data.string or r'繼續營業單位稅前淨利（淨損）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.profit_loss_from_continuing_operations_before_tax = st_to_decimal(next_data.string)
				elif r'所得稅費用（利益）合計' in data.string or r'所得稅（費用）利益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_tax_expense = st_to_decimal(next_data.string)
				elif r'繼續營業單位本期淨利（淨損）' in data.string or r'繼續營業單位本期稅後淨利（淨損）' in data.string or r'繼續營業單位淨利（淨損）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.profit_loss_from_continuing_operations = st_to_decimal(next_data.string)
				elif r'本期淨利（淨損）' in data.string or r'本期稅後淨利（淨損）' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						income_statement.profit_loss = st_to_decimal(next_data.string)
				elif r'國外營運機構財務報表換算之兌換差額' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.exchange_differences_on_translation = st_to_decimal(next_data.string)
				elif r'備供出售金融資產未實現評價損益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.unrealised_gains_losses_for_sale_financial_assets = st_to_decimal(next_data.string)
				elif r'採用權益法認列之關聯企業及合資之其他綜合損益之份額合計' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_share_of_other_income_of_associates_using_equity_method = st_to_decimal(next_data.string)
				elif r'與其他綜合損益組成部分相關之所得稅' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.income_tax_related_of_other_comprehensive_income = st_to_decimal(next_data.string)
				elif r'其他綜合損益（淨額）' in data.string or r'其他綜合損益（稅後）淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_other_comprehensive_income = st_to_decimal(next_data.string)
				elif r'其他綜合損益' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						income_statement.other_comprehensive_income = st_to_decimal(next_data.string)
				elif r'本期綜合損益總額' in data.string or r'本期綜合損益總額（稅後）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_comprehensive_income = st_to_decimal(next_data.string)
				elif r'母公司業主（淨利／損）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.profit_loss_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
				elif r'非控制權益（淨利／損）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.profit_loss_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
				elif r'母公司業主（綜合損益）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
				elif r'母公司業主' in data.string:
					if owners_of_parent == 0:
						next_data = data.next_sibling.next_sibling
						income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
						owners_of_parent = 1
					else:
						next_data = data.next_sibling.next_sibling
						income_statement.comprehensive_income_attributable_to_owners_of_parent = st_to_decimal(next_data.string)
				elif r'非控制權益（綜合損益）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.comprehensive_income_attributable_to_non_controlling_interests = st_to_decimal(next_data.string)
				elif r'基本每股盈餘' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						income_statement.total_basic_earnings_per_share = st_to_decimal(next_data.string)
				elif r'稀釋每股盈餘' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						income_statement.total_diluted_earnings_per_share = st_to_decimal(next_data.string)
				elif r'利息收入' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.interest_income = st_to_decimal(next_data.string)
				elif r'減：利息費用' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.interest_expenses = st_to_decimal(next_data.string)
				elif r'利息淨收益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_interest_income_expense = st_to_decimal(next_data.string)
				elif r'手續費淨收益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_service_fee_charge_and_commisions_income_loss = st_to_decimal(next_data.string)
				elif r'透過損益按公允價值衡量之金融資產及負債損益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.gain_loss_on_financial_assets_liabilities_at_fair_value = st_to_decimal(next_data.string)
				elif r'保險業務淨收益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_income_loss_of_insurance_operations = st_to_decimal(next_data.string)
				elif r'投資性不動產損益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.gain_loss_on_investment_property = st_to_decimal(next_data.string)
				elif r'備供出售金融資產之已實現損益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.realized_gains_on_available_for_sale_financial_assets = st_to_decimal(next_data.string)
				elif r'持有至到期日金融資產之已實現損益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.realized_gains_on_held_to_maturity_financial_assets = st_to_decimal(next_data.string)
				elif r'兌換損益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.foreign_exchange_gains_losses = st_to_decimal(next_data.string)
				elif r'資產減損（損失）迴轉利益淨額' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.impairment_loss_or_reversal_of_impairment_loss_on_assets = st_to_decimal(next_data.string)
				elif r'其他利息以外淨損益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_other_non_interest_incomes_losses = st_to_decimal(next_data.string)
				elif r'利息以外淨損益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_income_loss_except_interest = st_to_decimal(next_data.string)
				elif r'淨收益' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.net_income_loss = st_to_decimal(next_data.string)
				elif r'呆帳費用及保證責任準備提存（各項提存）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_bad_debts_expense_and_guarantee_liability_provisions = st_to_decimal(next_data.string)
				elif r'保險負債準備淨變動' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.total_net_change_in_provisions_for_insurance_liabilities = st_to_decimal(next_data.string)
				elif r'員工福利費用' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.employee_benefits_expenses = st_to_decimal(next_data.string)
				elif r'折舊及攤銷費用' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.employee_benefits_expenses = st_to_decimal(next_data.string)
				elif r'其他業務及管理費用' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.other_general_and_administrative_expenses = st_to_decimal(next_data.string)
				elif r'現金流量避險中屬有效避險不分之避險工具利益（損失）' in data.string:
					next_data = data.next_sibling.next_sibling
					income_statement.gain_loss_on_effective_portion_of_cash_flow_hedges = st_to_decimal(next_data.string)
				elif r'停業單位損益' in data.string or r'停業單位損益合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						income_statement.income_from_discontinued_operations = st_to_decimal(next_data.string)
			if income_statement.total_basic_earnings_per_share is not None:
				income_statement.save()
				print (stock_symbol + ' data updated ' + str(update_cnt) + ' in ' + str(len(stockIDs)))
			else:
				print (stock_symbol + 'has no data-----------')
				print (stock_symbol + 'time sleep')
				time.sleep(20)
	cnt = YearIncomeStatement.objects.filter(year=year).count()
	print('There is ' + str(cnt) + ' datas')
	lastDate = YearIncomeStatement.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = YearIncomeStatement.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='yis', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " yis in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year)})

	return HttpResponse(json_obj, content_type="application/json")

def update_year_cashflow_statement(request):
	print ('start update year income statement')
	if 'date' in request.GET:
		date = request.GET['date']
		if date != '':
			try:
				year = int(date)
			except:
				return HttpResponse('please input correct date "year"')
		else:
			return HttpResponse('please input correct date "year"')
	else:
		return HttpResponse('please input correct date "year"')
	stockIDs = get_updated_id(year, 4)
	update_cnt = 0
	for stock_id in stockIDs:
		update_cnt += 1
		stock_symbol = stock_id
		if not YearCashflowStatement.objects.filter(symbol=stock_symbol, year=year):
			print (stock_symbol + ' loaded ' + str(update_cnt) + ' in ' + str(len(stockIDs)))
			url = 'http://mops.twse.com.tw/mops/web/t164sb05'
			values = {'encodeURIComponent' : '1', 'id' : '', 'key' : '', 'TYPEK' : 'all', 'step' : '2',
					'year' : str(year-1911), 'season' : '4', 'co_id' : stock_symbol, 'firstin' : '1'}
			url_data = urllib.parse.urlencode(values).encode('utf-8')
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib.request.Request(url, url_data, headers)
			try:
				response = urllib.request.urlopen(req)
				soup = BeautifulSoup(response,from_encoding="utf-8")
				cashflos_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
				busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
			except urllib.error.URLError as e:
				busy_msg = True
				if hasattr(e, 'reason'):
					print(stock_id + ' not update. Reason:', e.reason)
			# 如果連線正常，還得再確認是否因查詢頻繁而給空表格；若有，則先sleep再重新連線
			while (busy_msg is not None):
				response.close()
				headers = {'User-Agent': 'Mozilla/5.0'}
				req = urllib.request.Request(url, url_data, headers)
				try:
					response = urllib.request.urlopen(req)
					soup = BeautifulSoup(response,from_encoding="utf-8")
					cashflos_datas = soup.find_all("td", {'style' : 'text-align:left;white-space:nowrap;'})
					busy_msg = soup.find('table', attrs = {'width':'80%', 'border':'0','cellspacing':'8'})
				except urllib.error.URLError as e:
					busy_msg = True
					if hasattr(e, 'reason'):
						print(stock_id + ' not update. Reason:', e.reason)
				if busy_msg:
					print (stock_symbol + ' time sleep')
					time.sleep(20)
			cashflow = YearCashflowStatement()
			cashflow.symbol = stock_symbol
			cashflow.year = str(year)
			cashflow.date = year_to_date(year)
			cashflow.surrogate_key = stock_symbol + '_' + str(year)
			for data in cashflos_datas:
				if data.string != None and (r'繼續營業單位稅前淨利（淨損）' in data.string or r'繼續營業單位稅前（淨利）淨損' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.profit_loss_from_continuing_operations_before_tax = st_to_decimal(next_data.string)
				if data.string != None and r'本期稅前淨利' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.profit_loss_before_tax = st_to_decimal(next_data.string)
				if data.string != None and r'折舊費用' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.depreciation_expense = st_to_decimal(next_data.string)
				if data.string != None and r'攤銷費用' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.amortization_expense = st_to_decimal(next_data.string)
				if data.string != None and r'利息費用' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_expense = st_to_decimal(next_data.string)
				if data.string != None and r'利息收入' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_income = st_to_decimal(next_data.string)
				if data.string != None and r'股份基礎給付酬勞成本' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.share_based_payments = st_to_decimal(next_data.string)
				if data.string != None and (r'採用權益法認列之關聯企業及合資損失（利益）之份額' in data.string or r'採用權益法認列之關聯企業及合資（損失）利益之份額' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.share_of_profit_loss_of_associates_using_equity_method = st_to_decimal(next_data.string)
				if data.string != None and (r'處分及報廢不動產、廠房及設備損失（利益）' in data.string or r'處分及報廢不動產、廠房及設備（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.loss_gain_on_disposal_of_property_plan_and_equipment = st_to_decimal(next_data.string)
				if data.string != None and (r'處分投資損失（利益）' in data.string or r'處分投資（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.loss_gain_on_disposal_of_investments = st_to_decimal(next_data.string)
				if data.string != None and (r'處分採用權益法之投資損失（利益）' in data.string or r'處分採用權益法之投資（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.loss_gain_on_disposal_of_investments_using_equity_method = st_to_decimal(next_data.string)
				if data.string != None and r'金融資產減損損失' in data.string and r'非' not in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.impairment_loss_on_financial_assets = st_to_decimal(next_data.string)
				if data.string != None and r'非金融資產減損損失' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.impairment_loss_on_non_financial_assets = st_to_decimal(next_data.string)
				if data.string != None and (r'已實現銷貨損失（利益）' in data.string or r'已實現銷貨（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.realized_loss_profit_on_from_sales = st_to_decimal(next_data.string)
				if data.string != None and (r'未實現外幣兌換損失（利益）' in data.string or r'未實現外幣兌換（損失）利益' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.unrealized_foreign_exchange_loss_gain = st_to_decimal(next_data.string)
				if data.string != None and r'其他項目' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.other_adjustments_to_reconcile_profit_loss = st_to_decimal(next_data.string)
				if data.string != None and r'不影響現金流量之收益費損項目合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_adjustments_to_reconcile_profit_loss = st_to_decimal(next_data.string)
				if data.string != None and (r'持有供交易之金融資產（增加）減少' in data.string or r'持有供交易之金融資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_financial_assets_held_for_trading = st_to_decimal(next_data.string)
				if data.string != None and (r'避險之衍生金融資產（增加）減少' in data.string or r'避險之衍生金融資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_derivative_financial_assets_for_hedging = st_to_decimal(next_data.string)
				if data.string != None and (r'應收帳款（增加）減少' in data.string or r'應收帳款增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_accounts_receivable = st_to_decimal(next_data.string)
				if data.string != None and (r'應收帳款－關係人（增加）減少' in data.string or r'應收帳款－關係人增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_accounts_receivable_from_related_parties = st_to_decimal(next_data.string)
				if data.string != None and (r'其他應收款－關係人（增加）減少' in data.string or r'其他應收款－關係人增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_other_receivable_due_from_related_parties = st_to_decimal(next_data.string)
				if data.string != None and (r'存貨（增加）減少' in data.string or r'存貨增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_inventories = st_to_decimal(next_data.string)
				if data.string != None and (r'其他流動資產（增加）減少' in data.string or r'其他流動資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_other_current_assets = st_to_decimal(next_data.string)
				if data.string != None and (r'其他金融資產（增加）減少' in data.string or r'其他金融資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_increase_in_other_financial_assets = st_to_decimal(next_data.string)
				if data.string != None and r'與營業活動相關之資產之淨變動合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_changes_in_operating_assets = st_to_decimal(next_data.string)
				if data.string != None and (r'應付帳款增加（減少）' in data.string or r'應付帳款（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_accounts_payable = st_to_decimal(next_data.string)
				if data.string != None and (r'應付帳款－關係人（增加）減少' in data.string or r'應付帳款－關係人增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_accounts_payable_to_related_parties = st_to_decimal(next_data.string)
				if data.string != None and (r'負債準備增加（減少）' in data.string or r'負債準備（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_provisions = st_to_decimal(next_data.string)
				if data.string != None and (r'其他流動負債增加（減少）' in data.string or r'其他流動負債（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_other_current_liabilities = st_to_decimal(next_data.string)
				if data.string != None and (r'應計退休金負債增加（減少）' in data.string or r'應計退休金負債（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_accrued_pension_liabilities = st_to_decimal(next_data.string)
				if data.string != None and (r'其他營業負債增加（減少）' in data.string or r'其他營業負債（增加）減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_decrease_in_other_operating_liabilities = st_to_decimal(next_data.string)
				if data.string != None and r'與營業活動相關之負債之淨變動合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_changes_in_operating_liabilities = st_to_decimal(next_data.string)
				if data.string != None and r'與營業活動相關之資產及負債之淨變動合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_changes_in_operating_assets_and_liabilities = st_to_decimal(next_data.string)
				if data.string != None and r'調整項目合計' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.total_adjustments = st_to_decimal(next_data.string)
				if data.string != None and (r'營運產生之現金流入（流出）' in data.string or r'營運產生之現金（流入）流出' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.cash_inflow_outflow_generated_from_operations = st_to_decimal(next_data.string)
				if data.string != None and (r'退還（支付）之所得稅' in data.string or r'（退還）支付之所得稅' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.income_taxes_refund_paid = st_to_decimal(next_data.string)
				if data.string != None and (r'營業活動之淨現金流入（流出）' in data.string or r'營業活動之淨現金（流入）流出' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.net_cash_flows_from_used_in_operating_activities = st_to_decimal(next_data.string)
				if data.string != None and r'取得備供出售金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_available_for_sale_financial_assets = st_to_decimal(next_data.string)
				if data.string != None and r'處分備供出售金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_available_for_sale_financial_assets = st_to_decimal(next_data.string)
				if data.string != None and r'取得持有至到期日金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_held_to_maturity_financial_assets = st_to_decimal(next_data.string)
				if data.string != None and r'持有至到期日金融資產到期還本' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_repayments_of_held_to_maturity_financial_assets = st_to_decimal(next_data.string)
				if data.string != None and r'取得以成本衡量之金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_financial_assets_at_cost = st_to_decimal(next_data.string)
				if data.string != None and r'處分以成本衡量之金融資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_financial_assets_at_cost = st_to_decimal(next_data.string)
				if data.string != None and r'處分採用權益法之投資' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_investments_using_equity_method = st_to_decimal(next_data.string)
				if data.string != None and r'處分子公司' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_subsidiaries = st_to_decimal(next_data.string)
				if data.string != None and r'取得不動產、廠房及設備' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_property_plant_and_equipment = st_to_decimal(next_data.string)
				if data.string != None and r'處分不動產、廠房及設備' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_disposal_of_property_plant_and_equipment = st_to_decimal(next_data.string)
				if data.string != None and r'存出保證金增加' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_refundable_deposits = st_to_decimal(next_data.string)
				if data.string != None and r'存出保證金減少' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_in_refundable_deposits = st_to_decimal(next_data.string)
				if data.string != None and r'取得無形資產' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.acquisition_of_intangible_assets = st_to_decimal(next_data.string)
				if data.string != None and (r'長期應收租賃款減少' in data.string or r'應收租賃款減少' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_in_long_term_lease_and_installment_receivables = st_to_decimal(next_data.string)
				if data.string != None and (r'其他金融資產增加' in data.string or r'其他金融資產（增加）減少' in data.string or r'其他金融資產增加（減少）' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_other_financial_assets = st_to_decimal(next_data.string)
				if data.string != None and r'其他非流動資產增加' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_other_non_current_assets = st_to_decimal(next_data.string)
				if data.string != None and r'收取之利息' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_received = st_to_decimal(next_data.string)
				if data.string != None and r'收取之股利' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.dividends_received = st_to_decimal(next_data.string)
				if data.string != None and r'其他投資活動' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.other_investing_activities = st_to_decimal(next_data.string)
				if data.string != None and (r'投資活動之淨現金流入（流出）' in data.string or r'投資活動之淨現金（流入）流出' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.net_cash_flows_from_used_in_investing_activities = st_to_decimal(next_data.string)
				if data.string != None and r'短期借款增加' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_short_term_loans = st_to_decimal(next_data.string)
				if data.string != None and r'發行公司債' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_issuing_bonds = st_to_decimal(next_data.string)
				if data.string != None and r'償還公司債' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.repayments_of_bonds = st_to_decimal(next_data.string)
				if data.string != None and r'舉借長期借款' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.proceeds_from_long_term_debt = st_to_decimal(next_data.string)
				if data.string != None and r'償還長期借款' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.repayments_of_long_term_debt = st_to_decimal(next_data.string)
				if data.string != None and r'存入保證金增加' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.increase_in_guarantee_deposits_received = st_to_decimal(next_data.string)
				if data.string != None and r'存入保證金減少' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_in_guarantee_deposits_received = st_to_decimal(next_data.string)
				if data.string != None and r'應付租賃款減少' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.decrease_in_lease_payable = st_to_decimal(next_data.string)
				if data.string != None and r'員工執行認股權' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.exercise_of_employee_share_options = st_to_decimal(next_data.string)
				if data.string != None and r'支付之利息' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_paid = st_to_decimal(next_data.string)
				if data.string != None and r'非控制權益變動' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.change_in_non_controlling_interests = st_to_decimal(next_data.string)
				if data.string != None and r'其他籌資活動' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.other_financing_activities = st_to_decimal(next_data.string)
				if data.string != None and (r'籌資活動之淨現金流入（流出）' in data.string or r'籌資活動之淨現金（流入）流出' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.net_cash_flows_from_used_in_financing_activities = st_to_decimal(next_data.string)
				if data.string != None and r'匯率變動對現金及約當現金之影響' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.effect_of_exchange_rate_changes_on_cash_and_cash_equivalents = st_to_decimal(next_data.string)
				if data.string != None and (r'本期現金及約當現金增加（減少）數' in data.string or r'本期現金及約當現金（增加）減少數' in data.string):
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.net_increase_decrease_in_cash_and_cash_equivalents = st_to_decimal(next_data.string)
				if data.string != None and r'期初現金及約當現金餘額' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.cash_and_cash_equivalents_at_beginning_of_period = st_to_decimal(next_data.string)
				if data.string != None and r'期末現金及約當現金餘額' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.cash_and_cash_equivalents_at_end_of_period = st_to_decimal(next_data.string)
				if data.string != None and r'資產負債表帳列之現金及約當現金' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.cash_and_cash_equivalents_in_the_statement_of_financial_position = st_to_decimal(next_data.string)
				cashflow.free_cash_flow = cashflow.net_cash_flows_from_used_in_operating_activities + cashflow.net_cash_flows_from_used_in_investing_activities
				if data.string != None and r'利息收入' in data.string:
					if data.next_sibling.next_sibling.string is not None:
						next_data = data.next_sibling.next_sibling
						cashflow.interest_income = st_to_decimal(next_data.string)
			response.close()
			if cashflow.profit_loss_from_continuing_operations_before_tax:
				cashflow.save()
	cnt = YearCashflowStatement.objects.filter(year=year).count()
	lastDate = YearCashflowStatement.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = YearCashflowStatement.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='ycs', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " ycs in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year)})

	return HttpResponse(json_obj, content_type="application/json")

def update_year_financial_ratio(request):
	print ('start update year financial ratio')
	if 'date' in request.GET:
		date = request.GET['date']
		if date != '':
			try:
				year = int(date)
			except:
				return HttpResponse('please input correct date "year"')
		else:
			return HttpResponse('please input correct date "year"')
	else:
		return HttpResponse('please input correct date "year"')
	yisSymbol = YearIncomeStatement.objects.filter(year=year).values_list('symbol', flat=True)
	ybsSymbol = SeasonBalanceSheet.objects.filter(year=year, season=4).values_list('symbol', flat=True)
	ycfSymbol = YearCashflowStatement.objects.filter(year=year).values_list('symbol', flat=True)
	union = set(yisSymbol).union(set(ybsSymbol)).union(set(ycfSymbol))
	intersection = set(yisSymbol).intersection(set(ybsSymbol)).intersection(set(ycfSymbol))
	diff = union.difference(intersection)
	print (diff)
	for stockID in intersection:
		#print 'update ' + stockID + "'s year financial ratio"
		has_ybs_prev = False
		try:
			yis = YearIncomeStatement.objects.get(year=year, symbol=stockID)
			ybs = SeasonBalanceSheet.objects.get(year=year, season=4, symbol=stockID)
			ycf = YearCashflowStatement.objects.get(year=year, symbol=stockID)
		except:
			print ("load " + stockID + "'s data error")
			continue
		if SeasonBalanceSheet.objects.filter(year=year-1, season=4, symbol=stockID):
			has_ybs_prev = True
			prev_ybs = SeasonBalanceSheet.objects.get(year=year-1, season=4, symbol=stockID)
		ratio = YearFinancialRatio()
		ratio.year = year
		ratio.symbol = stockID
		ratio.date = year_to_date(year)
		ratio.surrogate_key = stockID + '_' + str(year)
		if ybs.total_capital_stock and ybs.total_capital_stock > 0 and ybs.number_of_shares_in_entity_held_by_entity and ybs.number_of_shares_in_entity_held_by_entity > 0:
			total_stock = ybs.total_capital_stock - ybs.number_of_shares_in_entity_held_by_entity / 100
		elif ybs.total_capital_stock and ybs.total_capital_stock > 0:
			total_stock = ybs.total_capital_stock
		# 毛利率 = 營業毛利（毛損）淨額 / 營業收入合計（單位：％）
		if yis.total_operating_revenue and yis.total_operating_revenue > 0:
			if yis.gross_profit_loss_from_operations:
				ratio.gross_profit_margin = yis.gross_profit_loss_from_operations / yis.total_operating_revenue * 100
			# 有的公司使用舊式報表，沒有營業毛利這一項，就改用繼續營業單位稅前淨利代替
			elif yis.profit_loss_from_continuing_operations:
				ratio.gross_profit_margin = yis.profit_loss_from_continuing_operations / yis.total_operating_revenue * 100
		elif yis.total_operating_revenue and yis.total_operating_revenue == 0:
			ratio.gross_profit_margin = 0
		# 營業利益率 = 營業利益（損失） / 營業收入合計（單位：％）
		if yis.total_operating_revenue and yis.total_operating_revenue > 0:
			if yis.net_operating_income_loss:
				ratio.operating_profit_margin = yis.net_operating_income_loss / yis.total_operating_revenue * 100
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
			elif yis.profit_loss_from_continuing_operations:
				ratio.operating_profit_margin = yis.profit_loss_from_continuing_operations / yis.total_operating_revenue * 100
		elif yis.total_operating_revenue and yis.total_operating_revenue == 0:
			ratio.operating_profit_margin = 0
		# 稅前淨利率 = 稅前純益 / 營業收入
		if yis.total_operating_revenue and yis.total_operating_revenue > 0:
			if yis.profit_loss_from_continuing_operations_before_tax:
				ratio.net_profit_margin_before_tax = yis.profit_loss_from_continuing_operations_before_tax / yis.total_operating_revenue * 100
			elif yis.profit_loss_from_continuing_operations:
				ratio.net_profit_margin_before_tax = yis.profit_loss_from_continuing_operations / yis.total_operating_revenue * 100
		elif yis.total_operating_revenue and yis.total_operating_revenue == 0:
			ratio.net_profit_margin_before_tax = 0
		# 稅後淨利率 = 稅後純益 / 營業收入
		if yis.total_operating_revenue and yis.total_operating_revenue > 0:
			if yis.profit_loss:
				ratio.net_profit_margin = yis.profit_loss / yis.total_operating_revenue * 100
		elif yis.total_operating_revenue and yis.total_operating_revenue == 0:
			ratio.net_profit_margin = 0
		# 每股淨值(元)
		#net_value_per_share = models.DecimalField(max_digits=20, decimal_places=4, null=True)
		# 每股營業額(元)
		if ybs.total_capital_stock and ybs.total_capital_stock > 0:
			if yis.total_operating_revenue:
				ratio.revenue_per_share = yis.total_operating_revenue / total_stock * 10
		elif ybs.total_capital_stock and ybs.total_capital_stock == 0:
			ratio.revenue_per_share = 0
		# 每股營業利益(元)
		if ybs.total_capital_stock and ybs.total_capital_stock > 0:
			if yis.net_operating_income_loss:
				ratio.operating_profit_per_share = yis.net_operating_income_loss / total_stock * 10
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
			elif yis.profit_loss_from_continuing_operations:
				ratio.operating_profit_per_share = yis.profit_loss_from_continuing_operations / total_stock * 10
		elif ybs.total_capital_stock and ybs.total_capital_stock == 0:
			ratio.operating_profit_per_share = 0
		# 每股稅前淨利(元)
		if ybs.total_capital_stock and ybs.total_capital_stock > 0:
			if yis.profit_loss_from_continuing_operations_before_tax:
				ratio.net_before_tax_profit_per_share = yis.profit_loss_from_continuing_operations_before_tax / total_stock * 10
			elif yis.profit_loss_from_continuing_operations:
				ratio.net_before_tax_profit_per_share = yis.profit_loss_from_continuing_operations / total_stock
		elif ybs.total_capital_stock and ybs.total_capital_stock == 0:
			ratio.net_before_tax_profit_per_share = 0
		# 每股盈餘(EPS)
		if ybs.total_capital_stock and ybs.total_capital_stock > 0:
			if yis.profit_loss:
				ratio.earnings_per_share = yis.profit_loss / total_stock * 10
				ratio.earnings_per_share = yis.total_basic_earnings_per_share
		elif ybs.total_capital_stock == 0:
			ratio.earnings_per_share = 0
			ratio.earnings_per_share = yis.total_basic_earnings_per_share
		# 總資產報酬率(ROA) = 本期淨利（淨損） / 期初期末平均之資產總額（單位：％）
		if yis.profit_loss:
			if ycf.interest_expense:
				profitLoss = yis.profit_loss + ycf.interest_expense
			else:
				profitLoss = yis.profit_loss
			if ybs.total_assets:
				if has_ybs_prev:
					ratio.return_on_assets = profitLoss / ((ybs.total_assets + prev_ybs.total_assets) / 2) * 100
				else:
					ratio.return_on_assets = profitLoss / (ybs.total_assets / 2) * 100
			else:
				ratio.return_on_assets = 0
		# 股東權益報酬率(ROE) = 本期淨利(稅前) / 期初期末平均之權益總額(期初股東權益+期末股東權益/2)
		if yis.profit_loss:
			if ybs.total_equity:
				if has_ybs_prev and prev_ybs.total_equity:
					ratio.return_on_equity = yis.profit_loss / ((ybs.total_equity + prev_ybs.total_equity) / 2) * 100
				else:
					ratio.return_on_equity = yis.profit_loss / (ybs.total_equity / 2) * 100
			else:
				ratio.return_on_equity = 0
		# ---償債能力---
		# 流動比率 = 流動資產合計 / 流動負債合計
		if ybs.total_current_liabilities and ybs.total_current_liabilities != 0:
			if ybs.total_current_assets:
				ratio.current_ratio = ybs.total_current_assets / ybs.total_current_liabilities * 100
		# 速動比率 = 速動資產合計 / 流動負債合計（速動資產 = 流動資產 - 存貨 - 預付款項 - 其他流動資產）
		if ybs.total_current_liabilities and ybs.total_current_liabilities != 0:
			numerator = Decimal(0)
			if ybs.total_current_assets:
				numerator += ybs.total_current_assets
			if ybs.total_inventories:
				numerator -= ybs.total_inventories
			if ybs.total_prepayments:
				numerator -= ybs.total_prepayments
			if ybs.total_other_current_assets:
				numerator -= ybs.total_other_current_assets
			ratio.quick_ratio = numerator / ybs.total_current_liabilities * 100
		#?? 金融負債比率 = 金融負債總額 / 資產總額（金融負債 = 短期借款 + 應付短期票券 + 應付公司債 + 長期借款，要付息的，單位：％）
		#未完成
		if ybs.total_assets and ybs.total_assets != 0:
			numerator = Decimal(0)
			if ybs.total_short_term_borrowings:
				numerator += ybs.total_short_term_borrowings
			if ybs.short_term_notes_and_bills_payable:
				numerator += ybs.short_term_notes_and_bills_payable
			if ybs.total_bonds_payable:
				numerator += ybs.total_bonds_payable
			if ybs.total_long_term_borrowings:
				numerator += ybs.total_long_term_borrowings
			ratio.financial_debt_ratio = numerator / ybs.total_assets * 100
		# 負債比率
		if ybs.total_assets and ybs.total_assets != 0:
			if ybs.total_liabilities:
				ratio.debt_ratio = ybs.total_liabilities / ybs.total_assets * 100
		# 利息保障倍數
		if ycf.interest_expense and ycf.interest_expense != 0:
			if yis.profit_loss_from_continuing_operations_before_tax:
				ratio.interest_cover = (ycf.interest_expense + yis.profit_loss_from_continuing_operations_before_tax) / ycf.interest_expense
		# ---經營能力---
		# 應收帳款週轉率 = 營業收入合計 / 期初期末平均之應收票據淨額+應收帳款淨額+應收帳款－關係人淨額（單位：次／季）
		if yis.total_operating_revenue and yis.total_operating_revenue != 0:
			numerator = yis.total_operating_revenue
			denumerator = Decimal(0)
			if ybs.notes_receivable:
				denumerator += ybs.notes_receivable
			if ybs.accounts_receivable:
				denumerator += ybs.accounts_receivable
			if ybs.accounts_receivable_due_from_related_parties:
				denumerator += ybs.accounts_receivable_due_from_related_parties
			if has_ybs_prev:
				if prev_ybs.notes_receivable:
					denumerator += prev_ybs.notes_receivable
				if prev_ybs.accounts_receivable:
					denumerator += prev_ybs.accounts_receivable
				if prev_ybs.accounts_receivable_due_from_related_parties:
					denumerator += prev_ybs.accounts_receivable_due_from_related_parties
				denumerator /= 2
			if denumerator == 0:
				ratio.accounts_receivable_turnover_ratio = 0
			else:
				ratio.accounts_receivable_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.accounts_receivable_turnover_ratio = 0
		# 存貨週轉率 = 營業成本合計 / 期初期末平均之存貨（單位：次／季）
		if yis.total_operating_cost and yis.total_operating_cost != 0:
			numerator = yis.total_operating_cost
			denumerator = Decimal(0)
			if ybs.total_inventories:
				denumerator += ybs.total_inventories
			if has_ybs_prev:
				if prev_ybs.total_inventories:
					denumerator += prev_ybs.total_inventories
				denumerator /= 2
			if denumerator == 0:
				ratio.inventory_turnover_ratio = 0
			else:
				ratio.inventory_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.inventory_turnover_ratio = 0
		# 固定資產週轉率 = 營業收入合計 / 期初期末平均之不動產、廠房及設備（單位：次／季）
		if yis.total_operating_cost and yis.total_operating_cost != 0:
			numerator = yis.total_operating_cost
			denumerator = Decimal(0)
			if ybs.total_property_plant_and_equipment:
				denumerator += ybs.total_property_plant_and_equipment
			if has_ybs_prev:
				if prev_ybs.total_property_plant_and_equipment:
					denumerator += prev_ybs.total_property_plant_and_equipment
				denumerator /= 2
			if denumerator == 0:
				ratio.fixed_asset_turnover_ratio = 0
			else:
				ratio.fixed_asset_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.fixed_asset_turnover_ratio = 0
		# 總資產週轉率 = 營業收入合計 / 期初期末平均之資產總額（單位：次／季）
		if yis.total_operating_revenue and yis.total_operating_revenue != 0:
			numerator = yis.total_operating_revenue
			denumerator = Decimal(0)
			if ybs.total_assets:
				denumerator += ybs.total_assets
			if has_ybs_prev:
				if prev_ybs.total_assets:
					denumerator += prev_ybs.total_assets
				denumerator /= 2
			if denumerator == 0:
				ratio.total_asset_turnover_ratio = 0
			else:
				ratio.total_asset_turnover_ratio = numerator / denumerator * 4
		else:
			ratio.total_asset_turnover_ratio = 0
		# ---黃國華指標---
		# 存貨營收比 = 存貨 / 營業收入合計（評估存貨要多少季可以消化完畢，單位：季）
		if yis.total_operating_revenue and yis.total_operating_revenue != 0:
			if ybs.total_inventories:
				ratio.inventory_sales_ratio = ybs.total_inventories / yis.total_operating_revenue
			else:
				ratio.inventory_sales_ratio = 0
		else:
			ratio.inventory_sales_ratio = 0
		# 備供出售比率 = 備供出售金融資產－非流動淨額 / 權益總額（單位：％）
		if ybs.total_equity and ybs.total_equity != 0:
			if ybs.non_current_available_for_sale_financial_assets:
				ratio.available_for_sale_to_equity_ratio = ybs.non_current_available_for_sale_financial_assets / ybs.total_equity * 100
			else:
				ratio.available_for_sale_to_equity_ratio = 0
		else:
			ratio.available_for_sale_to_equity_ratio = 0
		# 無形資產比率 = 無形資產 / 權益總額（單位：％）
		if ybs.total_equity and ybs.total_equity != 0:
			if ybs.intangible_assets:
				ratio.intangible_asset_to_equity_ratio = ybs.intangible_assets / ybs.total_equity * 100
			else:
				ratio.intangible_asset_to_equity_ratio = 0
		else:
			ratio.intangible_asset_to_equity_ratio = 0
		# 折舊負擔比率 = 折舊費用 / 營業收入合計（評估營收必須拿多少來攤提折舊，單位：％）
		if yis.total_operating_revenue and yis.total_operating_revenue != 0:
			if ycf.depreciation_expense:
				ratio.depreciation_to_sales_ratio = ycf.depreciation_expense / yis.total_operating_revenue
			else:
				ratio.depreciation_to_sales_ratio = 1000
		else:
			ratio.depreciation_to_sales_ratio = 1000
		# 營業利益佔稅前淨利比率 = 營業利益（損失） / 稅前淨利（淨損）（單位：％）
		if yis.profit_loss_from_continuing_operations_before_tax and yis.profit_loss_from_continuing_operations_before_tax != 0:
			numerator = Decimal(0)
			if yis.net_operating_income_loss:
				numerator += yis.net_operating_income_loss
			# 有的公司使用舊式報表，沒有營業利益這一項，就改用繼續營業單位稅前淨利代替
			elif yis.profit_loss_from_continuing_operations_before_tax:
				numerator += yis.profit_loss_from_continuing_operations_before_tax
			ratio.operating_profit_to_net_profit_before_tax_ratio = numerator / yis.profit_loss_from_continuing_operations_before_tax
		# 現金股息配發率(季資料忽略此項目)
		# 營業稅率
		if yis.profit_loss_from_continuing_operations_before_tax and yis.profit_loss_from_continuing_operations_before_tax != 0:
			if yis.total_tax_expense:
				if yis.profit_loss_from_continuing_operations_before_tax < 0:
					ratio.tax_rate = -yis.total_tax_expense / yis.profit_loss_from_continuing_operations_before_tax
				else:
					ratio.tax_rate = yis.total_tax_expense / yis.profit_loss_from_continuing_operations_before_tax
			else:
				ratio.tax_rate = 0
		ratio.save()
		# print (ratio.symbol + " season financial ratio saved")
	cnt = YearFinancialRatio.objects.filter(year=year).count()
	lastDate = YearFinancialRatio.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = YearFinancialRatio.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='yfr', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " yfr in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year)})

	return HttpResponse(json_obj, content_type="application/json")

def update_data_date(request):
	objects = YearFinancialRatio.objects.all()
	for obj in objects:
		year = obj.year
		obj.data_date = financial_date_to_data_date(year, 4)
		obj.save()
	return HttpResponse("update ok")
