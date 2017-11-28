import datetime
import urllib.request
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
from decimal import Decimal
from stocks.models import MonthRevenue, StockId, SeasonRevenue
import pdb

def is_decimal(s):
	try:
		Decimal(s)
	except:
		return False
	return True

def st_to_decimal(data):
	return Decimal(data.strip().replace(',', ''))

# Create your views here.
def update_stockid(request):
	market_type = [2, 4]
	cnt = 0
	StockId.objects.all().delete()
	for mkt in market_type:
		url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=' + str(mkt)
		headers = {'User-Agent': 'Mozilla/5.0'}
		req = urllib.request.Request(url, None, headers)
		try:
			response = urllib.request.urlopen(req)
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
						company_type = tds[4].string.strip()
						stockid = StockId(symbol=symbol, name=name, market_type=market,
										  company_type=company_type, listing_date=listing_date)
						if symbol is not None:
							stockid.save()
							cnt += 1
							print("%s stockid is update" %(symbol))
	return HttpResponse("There are %d stockIds" %(cnt))

def update_month_revenue(request):
	if 'date' in request.GET:
		date = request.GET['date']
		try:
			str_year, str_month = date.split('-')
			year = int(str_year)
			month = int(str_month)
		except:
			return HttpResponse('please input correct date "year-mm"')
	else:
		return HttpResponse('please input correct date "year-mm"')
	market = ['sii', 'otc']
	for mkt in market:
		url = 'http://mops.twse.com.tw/nas/t21/' + mkt + '/t21sc03_' + str(year-1911) + '_' + str(month) + '_0.html'
		headers = {'User-Agent': 'Mozilla/5.0'}
		req = urllib.request.Request(url, None, headers)
		try:
			response = urllib.request.urlopen(req)
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
	return HttpResponse("There are %s month revenus on %s" %(cnt, date))
	#return HttpResponse(soup)

def update_season_revenue(request):
	if 'date' in request.GET:
		date = request.GET['date']
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
	return HttpResponse("Update %s season revenus on %s" %(cnt, date))

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