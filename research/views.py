#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from decimal import Decimal
import datetime
from django.http import HttpResponse
from django.db.models import Q, Max, Avg, Sum
from stocks.models import WatchList, StockId, Dividend, UpdateManagement, MonthRevenue
from prices.models import WeekPrice, PivotalPoint
from financial.models import SeasonFinancialRatio, YearFinancialRatio
from financial.models import *
from research.models import *
from core import util
from core.util import *
import csv
import pdb
import json

# Create your views here.
#wawa growth power
def update_wawa_growth_power(request):
	print ('start update wawa growth power')
	if 'date' in request.GET:
		date = request.GET['date']
		if date != '':
			try:
				str_year, str_season = date.split('-')
				year = int(str_year)
				season = int(str_season)
			except:
					return HttpResponse("please input correct season 'year-season'")
		else:
			return HttpResponse("please input correct season 'year-season'")
	else:
		return HttpResponse("please input correct season 'year-season'")
	stockids = WatchList.objects.values_list('symbol', flat=True).distinct()
	for stockid in stockids:
		#print("start " + stockid + "'s wawa growth power date:" + str_year + "-" + str_season)
		wawa_growth = WawaGrowthPower()
		wawa_growth.symbol = stockid
		wawa_growth.year = year
		wawa_growth.season = season
		wawa_growth.date = util.season_to_date(year, season)
		wawa_growth.surrogate_key = stockid + '_' + str(year) + str(season).zfill(2)
		if not SeasonFinancialRatio.objects.filter(symbol=stockid, year=year, season=season):
			print(stockid + "'s sfr is empty date:" + str_year + "-" + str_season)
			continue
		if not SeasonFinancialRatio.objects.filter(symbol=stockid, year=year-1, season=season):
			print(stockid + "'s sfr is empty date:" +str(year-1) + "-" + str_season)
			continue
		if not YearFinancialRatio.objects.filter(symbol=stockid, year=year-1):
			print(stockid + "'s yfr is empty year:" + str(year-1))
			continue
		if season == 1:
			financial_ratio = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season)
			wawa_growth.season_eps = financial_ratio.earnings_per_share
			wawa_growth.estimate_eps = wawa_growth.season_eps * 4
			wawa_growth.last_year_season_eps = SeasonFinancialRatio.objects.get(symbol=stockid, year=year-1, season=season).earnings_per_share
			wawa_growth.last_year_eps = YearFinancialRatio.objects.get(symbol=stockid, year=year-1).earnings_per_share
			if not wawa_growth.last_year_eps:
				continue
			wawa_growth.estimate_growth_rate = wawa_growth.estimate_eps / wawa_growth.last_year_eps - 1
			if (wawa_growth.estimate_growth_rate > 0.4):
				wawa_growth.estimate_growth_rate = Decimal(0.4)
			wawa_growth.reasonable_price = wawa_growth.estimate_growth_rate * Decimal(66) * wawa_growth.last_year_eps
			wawa_growth.save()
		elif season == 2:
			financial_ratio1 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season-1)
			financial_ratio2 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season)
			wawa_growth.season_eps = financial_ratio2.earnings_per_share
			wawa_growth.estimate_eps = (financial_ratio1.earnings_per_share + financial_ratio2.earnings_per_share) * 2
			wawa_growth.last_year_season_eps = SeasonFinancialRatio.objects.get(symbol=stockid, year=year-1, season=season).earnings_per_share
			wawa_growth.last_year_eps = YearFinancialRatio.objects.get(symbol=stockid, year=year-1).earnings_per_share
			if not wawa_growth.last_year_eps:
				continue
			wawa_growth.estimate_growth_rate = wawa_growth.estimate_eps / wawa_growth.last_year_eps - 1
			if (wawa_growth.estimate_growth_rate > 0.4):
				wawa_growth.estimate_growth_rate = Decimal(0.4)
			wawa_growth.reasonable_price = wawa_growth.estimate_growth_rate * Decimal(66) * wawa_growth.last_year_eps
			wawa_growth.save()
		elif season == 3:
			financial_ratio1 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season-2)
			financial_ratio2 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season-1)
			financial_ratio3 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season)
			wawa_growth.season_eps = financial_ratio3.earnings_per_share
			wawa_growth.estimate_eps = (financial_ratio1.earnings_per_share + financial_ratio2.earnings_per_share + financial_ratio3.earnings_per_share) * 4 / 3
			wawa_growth.last_year_season_eps = SeasonFinancialRatio.objects.get(symbol=stockid, year=year-1, season=season).earnings_per_share
			wawa_growth.last_year_eps = YearFinancialRatio.objects.get(symbol=stockid, year=year-1).earnings_per_share
			if not wawa_growth.last_year_eps:
				continue
			wawa_growth.estimate_growth_rate = wawa_growth.estimate_eps / wawa_growth.last_year_eps - 1
			if (wawa_growth.estimate_growth_rate > 0.4):
				wawa_growth.estimate_growth_rate = Decimal(0.4)
			wawa_growth.reasonable_price = wawa_growth.estimate_growth_rate * Decimal(66) * wawa_growth.last_year_eps
			wawa_growth.save()
		elif season == 4:
			try:
				financial_ratio1 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season-3)
				financial_ratio2 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season-2)
				financial_ratio3 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season-1)
				financial_ratio4 = SeasonFinancialRatio.objects.get(symbol=stockid, year=year, season=season)
				wawa_growth.season_eps = financial_ratio4.earnings_per_share
				wawa_growth.estimate_eps = financial_ratio1.earnings_per_share + financial_ratio2.earnings_per_share + \
										   financial_ratio3.earnings_per_share + financial_ratio4.earnings_per_share
				wawa_growth.last_year_season_eps = SeasonFinancialRatio.objects.get(symbol=stockid, year=year-1, season=season).earnings_per_share
				wawa_growth.last_year_eps = YearFinancialRatio.objects.get(symbol=stockid, year=year-1).earnings_per_share
			except:
				continue
			if not wawa_growth.last_year_eps:
				continue
			wawa_growth.estimate_growth_rate = wawa_growth.estimate_eps / wawa_growth.last_year_eps - 1
			if (wawa_growth.estimate_growth_rate > 0.4):
				wawa_growth.estimate_growth_rate = Decimal(0.4)
			wawa_growth.reasonable_price = wawa_growth.estimate_growth_rate * Decimal(66) * wawa_growth.estimate_eps
			wawa_growth.save()
		#print("update " + stockid + "'s wawa growth power date:" + str_year + "-" + str_season)
	cnt = WawaGrowthPower.objects.filter(year=year, season=season).count()
	print('There is ' + str(cnt) + ' datas')
	lastDate = WawaGrowthPower.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = WawaGrowthPower.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='waGrowth', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " wawa_growth in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(season)})

	return HttpResponse(json_obj, content_type="application/json")
	#return HttpResponse('update wawa_growth')

def update_vk_growth_power(request):
	print ('start update vk growth power')
	if 'date' in request.GET:
		date = request.GET['date']
		if date != '':
			try:
				str_year, str_season = date.split('-')
				year = int(str_year)
				season = int(str_season)
			except:
					return HttpResponse("please input correct season 'year-season'")
		else:
			return HttpResponse("please input correct season 'year-season'")
	else:
		return HttpResponse("please input correct season 'year-season'")
	stockids = WatchList.objects.values_list('symbol', flat=True).distinct()
	for stockid in stockids:
		vk_growth = VKGrowthPower()
		vk_growth.symbol = stockid
		vk_growth.year = year
		vk_growth.season = season
		vk_growth.date = util.season_to_date(year, season)
		vk_growth.surrogate_key = stockid + '_' + str(year) + str(season).zfill(2)
		if not SeasonFinancialRatio.objects.filter(symbol=stockid, year=year, season=season):
			print(stockid + "'s sfr is empty date:" + str_year + "-" + str_season)
			continue
		financial_ratios = SeasonFinancialRatio.objects.filter(symbol=stockid).order_by('-date')
		if (len(financial_ratios) >= 8):
			financial_ratio = financial_ratios[0]
			financial_ratio1 = financial_ratios[1]
			financial_ratio2 = financial_ratios[2]
			financial_ratio3 = financial_ratios[3]
			financial_ratio4 = financial_ratios[4]
			financial_ratio5 = financial_ratios[5]
			financial_ratio6 = financial_ratios[6]
			financial_ratio7 = financial_ratios[7]
			if not financial_ratio.earnings_per_share or not financial_ratio1.earnings_per_share or \
			   not financial_ratio2.earnings_per_share or not financial_ratio3.earnings_per_share or \
			   not financial_ratio4.earnings_per_share or not financial_ratio5.earnings_per_share or \
			   not financial_ratio6.earnings_per_share or not financial_ratio7.earnings_per_share:
			   continue
			vk_growth.season_eps = financial_ratio.earnings_per_share
			vk_growth.estimate_eps = financial_ratio.earnings_per_share + financial_ratio1.earnings_per_share + \
									 financial_ratio2.earnings_per_share + financial_ratio3.earnings_per_share
			vk_growth.last_year_season_eps = financial_ratio4.earnings_per_share
			vk_growth.last_year_eps = financial_ratio4.earnings_per_share + financial_ratio5.earnings_per_share + \
									  financial_ratio6.earnings_per_share + financial_ratio7.earnings_per_share
			vk_growth.estimate_growth_rate = vk_growth.estimate_eps / vk_growth.last_year_eps - 1
			if (vk_growth.estimate_growth_rate > 0.4):
				vk_growth.estimate_growth_rate = Decimal(0.4)
			vk_growth.reasonable_price = vk_growth.estimate_growth_rate * 66 * vk_growth.estimate_eps
			vk_growth.save()
			print("update " + stockid + "'s vk growth power date:" + str_year + "-" + str_season)
		else:
			print(stockid + "'s data not enough to update vk growth power")
	cnt = VKGrowthPower.objects.filter(year=year, season=season).count()
	print('There is ' + str(cnt) + ' datas')
	lastDate = VKGrowthPower.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = VKGrowthPower.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='vkGrowth', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " vk_growth in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(season)})

	return HttpResponse(json_obj, content_type="application/json")
	#return HttpResponse('update vk_growth date:' + str_year + "-"+ str_season)

def update_avg_pe(request):
	if 'year' in request.GET:
		str_year = request.GET['year']
		try:
			year = int(str_year)
		except:
			return HttpResponse("please input correct 'year'")
	else:
		return HttpResponse("please input correct 'year'")
	yfrs = YearFinancialRatio.objects.filter(year=year)
	for yfr in yfrs:
		print('update ' + yfr.symbol + "'s avg pe")
		max_price = 0;
		min_price = 1000000;
		prices = WeekPrice.objects.filter(symbol=yfr.symbol, date__year=year)
		for price in prices:
			if price.close_price > max_price:
				max_price = price.close_price
			if price.close_price < min_price:
				min_price = price.close_price
		avg_pe = AvgPE()
		avg_pe.surrogate_key = yfr.symbol + '_' + str(year)
		avg_pe.symbol = yfr.symbol
		avg_pe.year = year
		avg_pe.date = util.season_to_date(year, 1)
		avg_pe.low_price = min_price;
		avg_pe.high_price = max_price;
		avg_pe.eps = yfr.earnings_per_share
		if (avg_pe.eps > 0 and min_price < 1000000):
			avg_price = (avg_pe.low_price + avg_pe.high_price) / 2
			avg_pe.pe =  avg_price / avg_pe.eps
		else:
			avg_pe.pe = 1000000
		avg_pe.save()
		print("update " + yfr.symbol + "'s avg_pe year:" + str_year)
	return HttpResponse('update avg pe')

def update_wawa_value_line(request):
	if 'date' in request.GET:
		date = request.GET['date']
		if date != '':
			try:
				str_year, str_season = date.split('-')
				year = int(str_year)
				season = int(str_season)
			except:
					return HttpResponse("please input correct season 'year-season'")
		else:
			return HttpResponse("please input correct season 'year-season'")
	else:
		return HttpResponse("please input correct season 'year-season'")
	symbols = WatchList.objects.values_list('symbol', flat=True).distinct()
	for symbol in symbols:
		print("start update " + symbol + "'s value line date:" + str_year + "-" + str_season)
		value_line = WawaValueLine()
		value_line.surrogate_key = symbol + '_' + str_year
		value_line.symbol = symbol
		value_line.year = year
		value_line.season = season
		value_line.date = util.season_to_date(year, season)
		if not SeasonFinancialRatio.objects.filter(symbol=symbol, year=year, season=season):
			print(symbol + "'s sfr is empty date:" + str_year + "-" + str_season)
			continue
		sfrs = SeasonFinancialRatio.objects.filter(symbol=symbol).order_by('-date')
		if (len(sfrs) >= 4):
			value_line.last_year_eps = sfrs[0].earnings_per_share + sfrs[1].earnings_per_share + \
									   sfrs[2].earnings_per_share + sfrs[3].earnings_per_share
		else:
			continue
		yfrs = YearFinancialRatio.objects.filter(symbol=symbol).order_by('-date')
		len_yfrs = len(yfrs)
		value_line.future_eps_growth = Decimal(0.01)
		if (len_yfrs >=6):
			if (yfrs[5].earnings_per_share > 0):
				if (yfrs[0].earnings_per_share > yfrs[5].earnings_per_share):
					value_line.future_eps_growth = (yfrs[0].earnings_per_share / yfrs[5].earnings_per_share) ** (Decimal(1)/5)-1
				elif (yfrs[1].earnings_per_share > yfrs[5].earnings_per_share):
					value_line.future_eps_growth = (yfrs[1].earnings_per_share / yfrs[5].earnings_per_share) ** (Decimal(1)/4)-1
			elif (yfrs[4].earnings_per_share > 0):
				if (yfrs[0].earnings_per_share > yfrs[4].earnings_per_share):
					value_line.future_eps_growth = (yfrs[0].earnings_per_share / yfrs[4].earnings_per_share) ** (Decimal(1)/4) -1
				elif (yfrs[1].earnings_per_share > yfrs[4].earnings_per_share):
					value_line.future_eps_growth = (yfrs[1].earnings_per_share / yfrs[4].earnings_per_share) ** (Decimal(1)/3) -1
		elif (len_yfrs <= 1):
			value_line.future_eps_growth = Decimal(0.01)
		else:
			if (yfrs[len_yfrs-1].earnings_per_share > 0):
				if (yfrs[0].earnings_per_share > yfrs[len_yfrs-1].earnings_per_share):
					value_line.future_eps_growth = (yfrs[0].earnings_per_share / yfrs[len_yfrs-1].earnings_per_share) ** (Decimal(1)/(len_yfrs-1)) - 1
				elif (yfrs[1].earnings_per_share > yfrs[len_yfrs-1].earnings_per_share):
					value_line.future_eps_growth = (yfrs[1].earnings_per_share / yfrs[len_yfrs-1].earnings_per_share) ** (Decimal(1)/(len_yfrs-2)) - 1
			elif (yfrs[len_yfrs-2].earnings_per_share > 0):
				if (yfrs[0].earnings_per_share > yfrs[len_yfrs-2].earnings_per_share):
					value_line.future_eps_growth = (yfrs[0].earnings_per_share / yfrs[len_yfrs-2].earnings_per_share) ** (Decimal(1)/(len_yfrs-2)) - 1
				elif (yfrs[1].earnings_per_share > yfrs[len_yfrs-2].earnings_per_share):
					value_line.future_eps_growth = (yfrs[1].earnings_per_share / yfrs[len_yfrs-2].earnings_per_share) ** (Decimal(1)/(len_yfrs-3)) - 1
		avg_pes = AvgPE.objects.filter(symbol=symbol).order_by('-year')
		if (len(avg_pes) >= 6):
			value_line.past_pe = (avg_pes[0].pe + avg_pes[1].pe + avg_pes[2].pe + \
								 avg_pes[3].pe + avg_pes[4].pe) / 5
		elif (len(avg_pes) > 0):
			total_pe = 0
			for avg_pe in avg_pes:
				total_pe += avg_pe.pe
			value_line.past_pe = total_pe / (len(avg_pes))
		else:
			value_line.past_pe = 0
		if value_line.past_pe > 1000:
			value_line.past_pe = 0
		if (value_line.future_eps_growth > 0.3):
			value_line.future_eps_growth = Decimal(0.3)
		value_line.estimate_eps = value_line.last_year_eps * (Decimal(value_line.future_eps_growth+1) ** 10)
		value_line.estimate_future_price = value_line.estimate_eps * value_line.past_pe
		value_line.estimate_price = value_line.estimate_future_price / (Decimal(1.1) ** 10)
		value_line.hold_price = value_line.estimate_price * Decimal(0.8)
		dividends = Dividend.objects.filter(symbol=symbol,year__gte = year-5)
		total_dividend = 0
		if (len(dividends) > 0):
			for dividend in dividends:
				total_dividend += dividend.total_dividends
			value_line.avg_dividend = total_dividend / len(dividends)
		else:
			value_line.avg_dividend = 0
		value_line.low_price = 16 * value_line.avg_dividend
		value_line.high_price = 32 * value_line.avg_dividend
		one_year_dividend = Dividend.objects.filter(symbol=symbol).order_by('-date')
		if (len(one_year_dividend) > 0):
			value_line.one_low_price = 16 * one_year_dividend[0].total_dividends
		else:
			value_line.one_low_price = 0
		value_line.recovery_years = 100
		if (value_line.future_eps_growth > 0):
			eps_growth = value_line.future_eps_growth + 1
			total_value = 0
			for i in range(1, 15):
				total_value += value_line.last_year_eps * Decimal(eps_growth ** i)
				if total_value > value_line.hold_price:
					value_line.recovery_years = i
					break
		try:
			value_line.save()
		except:
			print (symbol + "'s value line save error")
	cnt = WawaValueLine.objects.filter(year=year, season=season).count()
	print('There is ' + str(cnt) + ' datas')
	lastDate = WawaValueLine.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = WawaValueLine.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='waValue', last_update_date = datetime.date.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " wawa_value_line in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(cnt) + ' data in ' + str(year) + '-' + str(season)})

	return HttpResponse(json_obj, content_type="application/json")

def down_load_growth(request):
	if 'season' in request.GET:
		season = request.GET['season']
		if season != '':
			try:
				str_year, str_season = season.split('-')
				year = int(str_year)
				season = int(str_season)
			except:
					return HttpResponse("please input correct season 'year-season'")
		else:
			return HttpResponse("please input correct season 'year-season'")
	else:
		return HttpResponse("please input correct season 'year-season'")
	try:
		request_date = request.GET['date']
		str_year, str_month, str_day = request_date.split('-')
		request_year = int(str_year)
		request_month = int(str_month)
		request_day =  int(str_day)
		date = datetime.date(request_year, request_month, request_day)
	except:
		date = datetime.date.today()
	data_date = date_to_revenue_date(date.year, date.month, date.day, 'month')
	response = HttpResponse(content_type='text/csv')
	today = datetime.datetime.today()
	filename = 'growth_power_' + str_year + str_season+'_' + today.strftime('%Y%m%d') + '.csv'
	response['Content-Disposition'] = 'attachment; filename=' + filename
	writer = csv.writer(response, delimiter=',', quotechar='"')
	header = ['StockID','Name','Note', 'User','Type','V', '5', 'Y', 'WG', 'VG', 'KP','PickTimes', 
			  'Price', 'PickPrice', '漲跌幅','EPS', 'PE', '月營收年增率', '累積營收年增率',
			  '3個月營收/12個月營收avg','季營益率','季淨利率','季營益率YOY','季EPS_YOY',
			  '連續現金股利','速動比','預估下個月營收年增率','近3年自由現金流','近8季盈益率max/min',
			  'recovery_year', 'hold_price', 'low_price', 'one_year_price', 'EPS_GrowthRate',
			  'SeasonEPS', 'LastYearSeasonEPS',
			  'W_ReasonablePrice', 'W_GrowthRate', 'W_EstiamteEPS', 'W_LastYearEPS', 
			  'V_ResonablePrice', 'V_GrowthRate', 'V_EstimateEPS', 'V_LastYearEPS']
	writer.writerow([x for x in header])
	season_date = today - datetime.timedelta(days=120)
	stockids = WatchList.objects.filter(Q(user='vk')|Q(user='wawa')|Q(date__gte=season_date)).values_list('symbol', flat=True)
	#query = reduce(operator.and_, (Q(symbol__contains=item) for item in stockids))
	symbols = StockId.objects.filter(symbol__in=stockids).order_by('company_type', 'symbol').values_list('symbol', flat=True)
	pivotal_point = PivotalPoint.objects.filter(date__gte=season_date)
	data_date_2month = month_minus(data_date, -2)
	data_date_11month = month_minus(data_date, -11)
	#symbols = StockId.objects.filter(query)
	for stockid in symbols:
		print (stockid)
		if (StockId.objects.filter(symbol__contains=stockid)):
			stockId = StockId.objects.get(symbol=stockid)
			body = [stockid]
			if stockid == '2353':
				body.append(u'宏碁')
			else:
				body.append(stockId.name)
			pick_in_six_months = WatchList.objects.filter(date__gte=season_date, symbol=stockid).order_by('-date')
			if (len(pick_in_six_months)>1):
				watchList = pick_in_six_months[0]
			else:
				watchList = WatchList.objects.filter(symbol=stockid).order_by('-date')[0]
			body.append('')
			body.append(watchList.user + '_' + watchList.date.strftime('%Y-%m-%d'))
			body.append(stockId.company_type)
			body.append('')
			body.append('')
			body.append('')
			body.append('')
			body.append('')
			#關鍵點
			if (pivotal_point.filter(symbol=stockid)):
				body.append(pivotal_point.filter(symbol=stockid).order_by('-date')[0].state)
			else:
				body.append('')
			#PickTimes
			body.append(str(len(pick_in_six_months)))
			#Price
			if (WeekPrice.objects.filter(symbol=stockid)):
				price = WeekPrice.objects.filter(symbol=stockid).order_by('-date')[0].close_price
				body.append(str(price))
			else:
				price = 0
				body.append('0')
			#LastPrice
			if (WeekPrice.objects.filter(symbol=stockid).count() >= 4):
				lastPrice = WeekPrice.objects.filter(symbol=stockid).order_by('-date')[4].close_price
				body.append(str(lastPrice))
			else:
				lastPrice = 0
				body.append('0')
			#4週漲跌幅
			if(price>0 and lastPrice >0):
				body.append("{0:.2%}".format((price / lastPrice)-1))
			else:
				body.append('NaN')
			#EPS
			seasonFinancialRatios = SeasonFinancialRatio.objects.filter(symbol=stockid).order_by('-date')
			if (seasonFinancialRatios.count() >= 5):
				try:
					body.append(seasonFinancialRatios[0].earnings_per_share + seasonFinancialRatios[1].earnings_per_share + \
								seasonFinancialRatios[2].earnings_per_share + seasonFinancialRatios[3].earnings_per_share)
				except:
					body.append('NaN')
			else:
				body.append('NaN')
			#pe
			if (WeekPrice.objects.filter(symbol=stockid)):
				price = WeekPrice.objects.filter(symbol=stockid).order_by('-date')[0]
			else:
				price = 0
			if (seasonFinancialRatios.count() > 3):
				try:
					eps = seasonFinancialRatios[0].earnings_per_share +\
						seasonFinancialRatios[1].earnings_per_share +\
						seasonFinancialRatios[2].earnings_per_share +\
						seasonFinancialRatios[3].earnings_per_share
					decimalPe = (price.close_price / eps)
					body.append(str('{0:.2f}'.format(decimalPe)))
				except:
					body.append('NaN')
			else:
				body.append('NaN')
			#月營收年增率
			#累計營收年增率
			if (MonthRevenue.objects.filter(symbol=stockid)):
				body.append(MonthRevenue.objects.filter(symbol=stockid).order_by('-date')[0].year_growth_rate)
				body.append(MonthRevenue.objects.filter(symbol=stockid).order_by('-date')[0].acc_year_growth_rate)
			else:
				body.append('')
				body.append('')
			#3個月營收/12個月營收avg
			near_3_month_revenue = MonthRevenue.objects.filter(symbol=stockid, data_date__lte=data_date, data_date__gte=data_date_2month)
			near_12_month_revenue = MonthRevenue.objects.filter(symbol=stockid, data_date__lte=data_date, data_date__gte=data_date_11month)
			if(near_3_month_revenue.count() == 3 and near_12_month_revenue.count()==12):
				three_month = near_3_month_revenue.aggregate(Avg('revenue'))['revenue__avg']
				twelve_month = near_12_month_revenue.aggregate(Avg('revenue'))['revenue__avg']
				body.append("{0:.1%}".format((three_month/twelve_month)-1))
			else:
				body.append('NaN')
			#季營益率
			body.append(seasonFinancialRatios[0].operating_profit_margin)
			#季淨利率
			body.append(seasonFinancialRatios[0].net_profit_margin_before_tax)
			#季營益率YOY
			if (seasonFinancialRatios.count() >= 5):
				try:
					body.append("{0:.1%}".format((seasonFinancialRatios[0].operating_profit_margin / seasonFinancialRatios[4].operating_profit_margin)-1))
				except:
					body.append('NaN')
			else:
				body.append('NaN')
			#季EPS_YOY
			if (seasonFinancialRatios.count() >= 5):
				try:
					body.append("{0:.1%}".format((seasonFinancialRatios[0].earnings_per_share / seasonFinancialRatios[4].earnings_per_share)-1))
				except:
					body.append('NaN')
			else:
				body.append('NaN')
			#連續現金股利
			dividends = Dividend.objects.filter(symbol=stockid).order_by('-date')
			dividend_con = 0
			if dividends.count() > 0:
				dividend_year = dividends[0].year + 1
			for dividend in dividends:
				if(dividend.cash_dividends > 0 and dividend.year == dividend_year-1):
					dividend_year = dividend.year
					dividend_con += 1
				else:
					break
			body.append(dividend_con)
			#速動比
			body.append(seasonFinancialRatios[0].quick_ratio)
			#預估下個月營收年增率
			try:
				this_month_revenue = MonthRevenue.objects.filter(symbol=stockid, data_date__lte=data_date).order_by('-data_date')[0].revenue
				last_eleven_month_revenue = MonthRevenue.objects.filter(symbol=stockid, data_date__lte=data_date).order_by('-data_date')[11].revenue
				body.append("{0:.1%}".format(this_month_revenue/last_eleven_month_revenue-1))
			except:
				body.append('NaN')
			#近3年自由現金流'
			yearCashflow = YearCashflowStatement.objects.filter(symbol=stockid).order_by('-date')
			if(yearCashflow.count()>=3):
				body.append(yearCashflow[0].net_cash_flows_from_used_in_operating_activities +\
				yearCashflow[1].net_cash_flows_from_used_in_operating_activities +\
				yearCashflow[2].net_cash_flows_from_used_in_operating_activities +\
				yearCashflow[0].net_cash_flows_from_used_in_investing_activities +\
				yearCashflow[1].net_cash_flows_from_used_in_investing_activities +\
				yearCashflow[2].net_cash_flows_from_used_in_investing_activities)
			else:
				body.append('NaN')
			#近8季盈益率max/min
			try:
				recent8SFR = SeasonFinancialRatio.objects.filter(symbol=stockid).order_by('-date')[:8]
				max_opm = 0
				min_opm = 0
				for sfr in recent8SFR:
					if(max_opm == 0 and min_opm == 0):
						max_opm = sfr.operating_profit_margin
						min_opm = sfr.operating_profit_margin
					else:
						if sfr.operating_profit_margin > max_opm:
							max_opm = sfr.operating_profit_margin
						if sfr.operating_profit_margin < min_opm:
							min_opm = sfr.operating_profit_margin
				body.append("{0:.1%}".format((max_opm / min_opm)-1))
			except:
				body.append('NaN')
			if (WawaValueLine.objects.filter(symbol=stockid, year=year)):
				value_line = WawaValueLine.objects.get(symbol=stockid, year=year)
				body.append(str(value_line.recovery_years))
				body.append('$'+str(value_line.hold_price))
				body.append('$'+str(value_line.low_price))
				body.append('$'+str(value_line.one_low_price))
				body.append(str(value_line.future_eps_growth))
			else:
				body.append('')
				body.append('')
				body.append('')
				body.append('')
				body.append('')
			if (WawaGrowthPower.objects.filter(symbol=stockid, year=year, season=season)):
				growth_power = WawaGrowthPower.objects.get(symbol=stockid, year=year, season=season)
				body.append('$'+str(growth_power.season_eps))
				body.append('$'+str(growth_power.last_year_season_eps))
				body.append('$'+str(growth_power.reasonable_price))
				body.append(str(growth_power.estimate_growth_rate))
				body.append('$'+str(growth_power.estimate_eps))
				body.append('$'+str(growth_power.last_year_eps))
			else:
				body.append('')
				body.append('')
				body.append('')
				body.append('')
				body.append('')
				body.append('')
			if (VKGrowthPower.objects.filter(symbol=stockid, year=year, season=season)):
				vk_growth_power = VKGrowthPower.objects.get(symbol=stockid, year=year, season=season)
				body.append('$'+str(vk_growth_power.reasonable_price))
				body.append(str(vk_growth_power.estimate_growth_rate))
				body.append('$'+str(vk_growth_power.estimate_eps))
				body.append('$'+str(vk_growth_power.last_year_eps))
			else:
				body.append('')
				body.append('')
				body.append('')
				body.append('')
			writer.writerow([x for x in body])
	return response