#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import urllib.request
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max
from bs4 import BeautifulSoup
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from stocks.models import *
from core.util import *
import json
import pdb
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def is_decimal(s):
	try:
		Decimal(s)
	except:
		return False
	return True

def st_to_decimal(data):
	return Decimal(data.strip().replace(',', ''))

# Create your views here.
@csrf_exempt
def update_stockid(request):
	market_type = [2, 4]
	cnt = 0
	StockId.objects.all().delete()
	for mkt in market_type:
		url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=' + str(mkt)
		headers = {'User-Agent': 'Mozilla/5.0'}
		req = urllib.request.Request(url, None, headers)
		context = ssl._create_unverified_context()
		try:
			response = urllib.request.urlopen(req, context=context)
		except urllib.error.URLError as e:
			print(mkt + ' not update. Reason:', e.reason)
		else:
			if mkt == 2:
				market = 'sii'
			elif mkt == 4:
				market = 'otc'
			html = response.read()
			soup = BeautifulSoup(html.decode("cp950", "ignore"), "html.parser")
			trs = soup.find_all('tr')
			for tr in trs:
				tds = tr.find_all('td')
				if len(tds) == 7:
					if tds[5].string == 'ESVUFR' or tds[5].string == 'ESVTFR':
						symbol, name = tds[0].string.split()
						symbol = symbol.strip()
						name = name.strip()
						listing_date = datetime.datetime.strptime(tds[2].string.strip(), '%Y/%m/%d').date()
						try:
							company_type = tds[4].string.strip()
						except:
							content_type = "nil"
						stockid = StockId(symbol=symbol, name=name, market_type=market,
										  company_type=company_type, listing_date=listing_date)
						if symbol is not None:
							stockid.save()
							cnt += 1
							print("%s stockid is update" %(symbol))
	lastDate = datetime.date.today()
	lastDateDataCnt = cnt
	updateManagement = UpdateManagement(name='sid', last_update_date = lastDate,
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " stockid in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + lastDate.strftime("%Y-%m-%d")})

	return HttpResponse(json_obj, content_type="application/json")

@csrf_exempt
def update_month_revenue(request):
	if 'date' in request.POST:
		date = request.POST['date']
		try:
			str_year, str_month = date.split('-')
			year = int(str_year)
			month = int(str_month)
		except:
			return HttpResponse('please input correct date "year-mm"')
	else:
		return HttpResponse('no input date please input correct date "year-mm"')
	market = ['sii', 'otc']
	for mkt in market:
		ssl._create_default_https_context = ssl._create_unverified_context
		for i in ['0','1']:
			url = 'https://mops.twse.com.tw/nas/t21/' + mkt + '/t21sc03_' + str(year-1911) + '_' + str(month) + '_' + i + '.html'
			headers = {'User-Agent': 'Mozilla/5.0'}
			#req = urllib.request.Request(url, None, headers)
			try:
				print('start parse '+url)
				#context = ssl._create_unverified_context()
				response = urllib.request.urlopen(url)
				html = response.read()
				soup = BeautifulSoup(html.decode("cp950", "ignore"), "html.parser")
				trs = soup.find_all('tr', {'align': 'right'})
				for tr in trs:
					tds = tr.find_all('td')
					if (len(tds) == 11):
						revenue = MonthRevenue()
						revenue.surrogate_key = tds[0].string.strip() + "_" + str(year) + str(month).zfill(2)
						revenue.year = year
						revenue.month = month
						revenue.date = datetime.date(year, month, 1)
						revenue.data_date = revenue_date_to_data_date(year, month)
						revenue.symbol = tds[0].string.strip()
						if is_decimal(st_to_decimal(tds[2].string.strip())):
							revenue.revenue = tds[2].string.strip().replace(',', '')
						if is_decimal(tds[4].string.strip().replace(',', '')):
							revenue.last_year_revenue = tds[4].string.strip().replace(',', '')
						if is_decimal(tds[5].string.strip().replace(',', '')):
							revenue.month_growth_rate = tds[5].string.strip().replace(',', '')
						if is_decimal(tds[6].string.strip().replace(',', '')):
							revenue.year_growth_rate = tds[6].string.strip().replace(',', '')
						if is_decimal(tds[7].string.strip().replace(',', '')):
							revenue.acc_revenue = tds[7].string.strip().replace(',', '')
						if is_decimal(tds[9].string.strip().replace(',', '')):
							revenue.acc_year_growth_rate = tds[9].string.strip().replace(',', '')
						revenue.save()
			except urllib.error.URLError as e:
				print(mkt + ' not update. Reason:', e.reason)
	cnt = MonthRevenue.objects.filter(year=year, month=month).count()
	lastDate = MonthRevenue.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = MonthRevenue.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='mr', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " month_revenues in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(month)})

	return HttpResponse(json_obj, content_type="application/json")
	#return HttpResponse(soup)
@csrf_exempt
def update_season_revenue(request):
	if 'date' in request.POST:
		date = request.POST['date']
		try:
			str_year, str_season = date.split('-')
			year = int(str_year)
			season = int(str_season)
		except:
			return HttpResponse('please input correct date "year-season"')
	else:
		return HttpResponse('please input correct date "year-season"')
	startMonthLsit = [1, 4, 7, 10]
	startMonth = int(season-1) * 3 + 1
	if (startMonth not in startMonthLsit):
		return HttpResponse('please input correct date "year-season"')
	firstMonthStockIds = MonthRevenue.objects.filter(year=year, month=startMonth).values_list('symbol', flat=True)
	secondMonthStockIds = MonthRevenue.objects.filter(year=year, month=startMonth+1).values_list('symbol', flat=True)
	thirdMonthStockIds = MonthRevenue.objects.filter(year=year, month=startMonth+2).values_list('symbol', flat=True)
	firstMonthRevenue = MonthRevenue.objects.filter(year=year, month=startMonth)
	secondMonthRevenue = MonthRevenue.objects.filter(year=year, month=startMonth+1)
	thirdMonthRevenue = MonthRevenue.objects.filter(year=year, month=startMonth+2)
	date = datetime.date(year, startMonth, 1)
	data_date = revenue_date_to_data_date(year, startMonth+2)
	lastYear, lastSeason = last_season(date)
	lastSeasonRevenues = SeasonRevenue.objects.filter(year=lastYear, season=lastSeason)
	symbols = list(set(firstMonthStockIds).intersection(set(secondMonthStockIds)).intersection(set(thirdMonthStockIds)))
	for symbol in symbols:
		revenue = SeasonRevenue()
		revenue.surrogate_key = symbol + '_' + str(year) + str(season).zfill(2)
		revenue.year = year
		revenue.season = season
		revenue.date = date
		revenue.symbol = symbol
		revenue.data_date = data_date
		try:
			revenue.revenue = firstMonthRevenue.get(symbol=symbol).revenue +\
							  secondMonthRevenue.get(symbol=symbol).revenue +\
							  thirdMonthRevenue.get(symbol=symbol).revenue
			revenue.last_year_revenue = firstMonthRevenue.get(symbol=symbol).last_year_revenue +\
										secondMonthRevenue.get(symbol=symbol).last_year_revenue +\
										thirdMonthRevenue.get(symbol=symbol).last_year_revenue
			if revenue.last_year_revenue > 0:
				revenue.year_growth_rate = revenue.revenue / revenue.last_year_revenue * 100 - 100
			if lastSeasonRevenues.filter(symbol=symbol):
				last_season_revenue = lastSeasonRevenues.get(symbol=symbol).revenue
				if last_season_revenue > 0:
					revenue.season_growth_rate = revenue.revenue / last_season_revenue * 100 - 100
			revenue.acc_revenue = thirdMonthRevenue.get(symbol=symbol).acc_revenue
			revenue.acc_year_growth_rate = thirdMonthRevenue.get(symbol=symbol).acc_year_growth_rate
			revenue.save()
		except:
			pass
	cnt = SeasonRevenue.objects.filter(year=year, season=season).count()
	lastDate = SeasonRevenue.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = SeasonRevenue.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='sr', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " season_revenues in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(season)})
	return HttpResponse(json_obj, content_type="application/json")
	#return HttpResponse("Update %s season revenus on %s" %(cnt, date))

def last_season(day):
	year = day.year
	month = day.month
	if month <= 3:
		season = 4
		year -= 1
	elif month >= 4 and month <= 6:
		season = 1
	elif month >= 7 and month <= 9:
		season = 2
	elif month >= 10:
		season = 3
	return year, season

def update_dividend(request):
	if 'year' in request.GET:
		input_year = int(request.GET['year'])
	else:
		input_year = 2016
	stock_ids = StockId.objects.all()
	for stock_id in stock_ids:
		dividendInDb = Dividend.objects.filter(symbol=stock_id.symbol, year=int(input_year))
		if dividendInDb:
			continue
		else:
			stock_symbol = stock_id.symbol
			url = "http://jsjustweb.jihsun.com.tw/z/zc/zcc/zcc_" + stock_symbol + ".djhtm"
			headers = {'User-Agent': 'Mozilla/5.0'}
			req = urllib.request.Request(url, None, headers)
			response = urllib.request.urlopen(req)
			html = response.read()
			soup = BeautifulSoup(html.decode("cp950", "ignore"), "html.parser")
			dividend_datas = soup.find_all("td", { "class": ["t3n0", "t3n1"] })
			for dividend_data in dividend_datas:
				if (dividend_data['class'][0] == 't3n0'):
					try:
						year = int(dividend_data.string)
						dividend = Dividend()
						dividend.year = year
						dividend.date = datetime.date(year, 1, 1)
						dividend.surrogate_key = stock_symbol + "_" + str(year)
						dividend.symbol = stock_symbol
						next = dividend_data.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
						dividend.cash_dividends = Decimal(next.string)
						next = next.next_sibling.next_sibling
						dividend.stock_dividends_from_retained_earnings = Decimal(next.string)
						next = next.next_sibling.next_sibling
						dividend.stock_dividends_from_capital_reserve = Decimal(next.string)
						next = next.next_sibling.next_sibling
						dividend.stock_dividends = Decimal(next.string)
						next = next.next_sibling.next_sibling
						dividend.total_dividends = Decimal(next.string)
						next = next.next_sibling.next_sibling
						dividend.employee_stock_rate = Decimal(next.string)
						dividend.save()
					except:
						pass
			print ('update ' + stock_symbol + ' dividend')
	return HttpResponse("update dividend")

def update(request):
	all_data = UpdateManagement.objects.all()
	sid = {}
	mr = {}
	sr = {}
	sis = {}
	sbs = {}
	scs = {}
	sfr = {}
	yis = {}
	ycs	 = {}
	yfr = {}
	wp = {}
	kp = {}
	waGrowth = {}
	waValue = {}
	vkGrowth = {}
	#綜合損益表(季)
	#資產負債表(季)
	#現金流量表(季)
	#財務比率(季)
	#綜合損益表(年)
	#現金流量表(年)
	#財務比率(年)
	if all_data.filter(name='sid').count() > 0:
		data = UpdateManagement.objects.get(name='sid')
		sid['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		sid['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		sid['note'] = data.notes
	if all_data.filter(name='mr').count() > 0:
		data = UpdateManagement.objects.get(name='mr')
		mr['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		mr['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		mr['note'] = data.notes
	if all_data.filter(name='sr').count() > 0:
		data = UpdateManagement.objects.get(name='sr')
		sr['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		sr['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		sr['note'] = data.notes
	if all_data.filter(name='sis').count() > 0:
		data = UpdateManagement.objects.get(name='sis')
		sis['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		sis['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		sis['note'] = data.notes
	if all_data.filter(name='sbs').count() > 0:
		data = UpdateManagement.objects.get(name='sbs')
		sbs['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		sbs['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		sbs['note'] = data.notes
	if all_data.filter(name='scs').count() > 0:
		data = UpdateManagement.objects.get(name='scs')
		scs['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		scs['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		scs['note'] = data.notes
	if all_data.filter(name='sfr').count() > 0:
		data = UpdateManagement.objects.get(name='sfr')
		sfr['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		sfr['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		sfr['note'] = data.notes
	if all_data.filter(name='yis').count() > 0:
		data = UpdateManagement.objects.get(name='yis')
		yis['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		yis['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		yis['note'] = data.notes
	if all_data.filter(name='ycs').count() > 0:
		data = UpdateManagement.objects.get(name='ycs')
		ycs['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		ycs['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		ycs['note'] = data.notes
	if all_data.filter(name='yfr').count() > 0:
		data = UpdateManagement.objects.get(name='yfr')
		yfr['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		yfr['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		yfr['note'] = data.notes
	if all_data.filter(name='wp').count() > 0:
		data = UpdateManagement.objects.get(name='wp')
		wp['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		wp['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		wp['note'] = data.notes
	if all_data.filter(name='kp').count() > 0:
		data = UpdateManagement.objects.get(name='kp')
		kp['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		kp['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		kp['note'] = data.notes
	if all_data.filter(name='waGrowth').count() > 0:
		data = UpdateManagement.objects.get(name='waGrowth')
		waGrowth['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		waGrowth['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		waGrowth['note'] = data.notes
	if all_data.filter(name='waValue').count() > 0:
		data = UpdateManagement.objects.get(name='waValue')
		waValue['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		waValue['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		waValue['note'] = data.notes
	if all_data.filter(name='vkGrowth').count() > 0:
		data = UpdateManagement.objects.get(name='vkGrowth')
		vkGrowth['update_date'] = data.last_update_date.strftime("%Y-%m-%d")
		vkGrowth['data_date'] = data.last_data_date.strftime("%Y-%m-%d")
		vkGrowth['note'] = data.notes
	return render(request, 'update.html', {
		'mr': mr,
		'sr': sr,
		'sis': sis,
		'sbs': sbs,
		'scs': sbs,
		'sfr': sfr,
		'yis': yis,
		'ycs': ycs,
		'yfr': yfr,
		'sid': sid,
		'wp': wp,
		'kp': kp,
		'waGrowth' : waGrowth,
		'waValue' : waValue,
		'vkGrowth' : vkGrowth,
	})

def jquery_test(request):
	return render(request, 'jquery_test.html')
