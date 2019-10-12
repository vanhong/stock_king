#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max, Q
import urllib
import pdb
from decimal import Decimal
from datetime import *
from datetime import timedelta
from stocks.models import StockId, WatchList
from prices.models import WeekPrice, PivotalPoint
from prices.pivotal_state import *
from stocks.models import UpdateManagement
import json
import csv

INIT_PIVOTAL_STATE = 'init_pivotal_state'
UPWARD_TREND_STATE = 'upward_trend_state'
DOWNWARD_TREND_STATE = 'downward_trend_state'
NATURAL_REACTION_STATE = 'natural_reaction_state'
NATURAL_RALLY_STATE = 'natural_rally_state'
SECONDARY_REACTION_STATE = 'secondary_reaction_state'
SECONDARY_RALLY_STATE = 'secondary_rally_state'

# Create your views here.
def show_price(request):
	url = 'http://jsjustweb.jihsun.com.tw/Z/ZC/ZCW/czkc1.djbcd?a=2383&b=W&c=2880&E=1&ver=5'
	headers = {'User-Agent': 'Mozilla/5.0'}
	req = urllib.request.Request(url, None, headers)
	response = urllib.request.urlopen(req)
	#response = urllib.urlopen(url)
	data = response.read()
	array = data.split()
	data1 = array[0].split(b',')
	data2 = array[1].split(b',')
	data3 = array[2].split(b',')
	data4 = array[3].split(b',')
	data5 = array[4].split(b',')
	data6 = array[5].split(b',')
	#bytes to string str(bstring, 'utf-8')
	return HttpResponse(data)

def new_update_price(request):
	stockids = ['8109']
	start = datetime(2016,1,1)
	end = date.today()
	prices = web.DataReader('8109.TWO', 'yahoo', start, end)
	today = datetime.today()
	monday = start - timedelta(days=today.weekday())
	sunday = monday + timedelta(6)
	print(monday)
	print(sunday)
	print (prices.head())
	return HttpResponse('update price')

def update_price(request):
	stockids = StockId.objects.all()
	symbol_cnt = 0;
	today = datetime.today()
	last_monday = today - timedelta(days=today.weekday())
	if 'date' in request.GET:
		date = request.GET['date']
		last_monday = datetime.strptime(date, '%Y-%m-%d')
	for stockid in stockids:
		print ('start update {0} history price'.format(stockid.symbol))
		lastest_price_date = WeekPrice.objects.filter(symbol=stockid.symbol).aggregate(Max('date'))
		if lastest_price_date['date__max'] == None:
			pass
		elif last_monday.date() <= lastest_price_date['date__max']:
			continue
		url = 'http://jsjustweb.jihsun.com.tw/Z/ZC/ZCW/czkc1.djbcd?a=' + stockid.symbol + '&b=W&c=2880&E=1&ver=5'
		response = urllib.request.urlopen(url)
		datas = response.read().split()
		if (len(datas) >=6):
			dates = datas[0].split(b',')
			opens = datas[1].split(b',')
			highs = datas[2].split(b',')
			lows = datas[3].split(b',')
			closes = datas[4].split(b',')
			volumes = datas[5].split(b',')
		else:
			continue
		cnt = 0
		for i in range(len(dates)):
			priceObj = WeekPrice()
			priceObj.surrogate_key = stockid.symbol + '_' + str(dates[i].decode('utf-8')).replace('/','-')
			priceObj.date = datetime.strptime(str(dates[i], 'utf-8'), '%Y/%m/%d').date()
			priceObj.symbol = stockid.symbol
			priceObj.open_price = Decimal(str(opens[i], 'utf-8'))
			priceObj.high_price = Decimal(str(highs[i], 'utf-8'))
			priceObj.low_price = Decimal(str(lows[i], 'utf-8'))
			priceObj.close_price = Decimal(str(closes[i], 'utf-8'))
			priceObj.volume = Decimal(str(volumes[i], 'utf-8'))
			priceObj.save()
			cnt = cnt + 1
		symbol_cnt = symbol_cnt + 1
		print ('update {0} history price, there has {1} datas'.format(stockid.symbol, cnt))
	#lastDate = WeekPrice.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = WeekPrice.objects.filter(date__gte=last_monday).count()
	updateManagement = UpdateManagement(name='wp', last_update_date = datetime.today(),
										last_data_date = last_monday, 
										notes = "There is " + str(lastDateDataCnt) + " week price after " + last_monday.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': last_monday.strftime("%Y-%m-%d"), 'notes': 'update ' + str(lastDateDataCnt) + ' data in ' + last_monday.strftime("%Y-%m-%d")})

	return HttpResponse(json_obj, content_type="application/json")

def update_pivotal_state(request):
	stock_ids = StockId.objects.all()
	for stock_id in stock_ids:
		cnt = 0
		pivotal_point_count = PivotalPoint.objects.filter(symbol=stock_id.symbol).count()
		print("start update {0} pivotal".format(stock_id.symbol))
		if pivotal_point_count < 10:
			stock_prices = WeekPrice.objects.filter(symbol=stock_id.symbol).order_by('date')
			if stock_prices.count() == 0:
				print ("update {0} pivotal error, there is no price data".format(stock_id))
				continue
			pivotal_state = InitPivotalState(date=stock_prices[0].date.strftime('%Y-%m-%d'), price=0, symbol=stock_id.symbol, prev_state='init_pivotal_state', upward_trend=0 ,\
											downward_trend=0, natural_reaction=0, natural_rally=0, secondary_rally=0, secondary_reaction=0)
			for stock_price in stock_prices:
				cnt += 1
				pivotal_state = pivotal_state.next(stock_price.close_price, stock_price.date.strftime('%Y-%m-%d'))
				pivotal_state.save_to_db()
			print ('update {0} pivotal state, there has {1} datas'.format(stock_id.symbol, cnt))
		else:
			pivotal_state = PivotalPoint.objects.filter(symbol=stock_id.symbol).order_by("-date")[9]
			stock_prices = WeekPrice.objects.filter(symbol=stock_id.symbol, date__gte=pivotal_state.date).order_by("date")
			if (pivotal_state.date != stock_prices[0].date):
				print ("update {0} pivotal error date is not the same".format(stock_id))
			else:
				if pivotal_state.state == INIT_PIVOTAL_STATE:
					pivotal_state = InitPivotalState(date=pivotal_state.date.strftime('%Y-%m-%d'), price=pivotal_state.price, symbol=stock_id.symbol, prev_state=pivotal_state.prev_state, \
													 upward_trend=pivotal_state.upward_trend_point , downward_trend=pivotal_state.downward_trend_point, natural_reaction=pivotal_state.natural_reaction_point, \
													 natural_rally=pivotal_state.natural_rally_point, secondary_rally=pivotal_state.secondary_rally_point, secondary_reaction=pivotal_state.secondary_reaction_point)
				elif pivotal_state.state == UPWARD_TREND_STATE:
					pivotal_state = UpwardTrendState(date=pivotal_state.date.strftime('%Y-%m-%d'), price=pivotal_state.price, symbol=stock_id.symbol, prev_state=pivotal_state.prev_state, \
													 upward_trend=pivotal_state.upward_trend_point , downward_trend=pivotal_state.downward_trend_point, natural_reaction=pivotal_state.natural_reaction_point, \
													 natural_rally=pivotal_state.natural_rally_point, secondary_rally=pivotal_state.secondary_rally_point, secondary_reaction=pivotal_state.secondary_reaction_point)
				elif pivotal_state.state == DOWNWARD_TREND_STATE:
					pivotal_state = DownwardTrendState(date=pivotal_state.date.strftime('%Y-%m-%d'), price=pivotal_state.price, symbol=stock_id.symbol, prev_state=pivotal_state.prev_state, \
													 upward_trend=pivotal_state.upward_trend_point , downward_trend=pivotal_state.downward_trend_point, natural_reaction=pivotal_state.natural_reaction_point, \
													 natural_rally=pivotal_state.natural_rally_point, secondary_rally=pivotal_state.secondary_rally_point, secondary_reaction=pivotal_state.secondary_reaction_point)
				elif pivotal_state.state == NATURAL_RALLY_STATE:
					pivotal_state = NaturalRallyState(date=pivotal_state.date.strftime('%Y-%m-%d'), price=pivotal_state.price, symbol=stock_id.symbol, prev_state=pivotal_state.prev_state, \
													 upward_trend=pivotal_state.upward_trend_point , downward_trend=pivotal_state.downward_trend_point, natural_reaction=pivotal_state.natural_reaction_point, \
													 natural_rally=pivotal_state.natural_rally_point, secondary_rally=pivotal_state.secondary_rally_point, secondary_reaction=pivotal_state.secondary_reaction_point)
				elif pivotal_state.state == NATURAL_REACTION_STATE:
					pivotal_state = NaturalReactionState(date=pivotal_state.date.strftime('%Y-%m-%d'), price=pivotal_state.price, symbol=stock_id.symbol, prev_state=pivotal_state.prev_state, \
													 upward_trend=pivotal_state.upward_trend_point , downward_trend=pivotal_state.downward_trend_point, natural_reaction=pivotal_state.natural_reaction_point, \
													 natural_rally=pivotal_state.natural_rally_point, secondary_rally=pivotal_state.secondary_rally_point, secondary_reaction=pivotal_state.secondary_reaction_point)
				elif pivotal_state.state == SECONDARY_RALLY_STATE:
					pivotal_state = SecondaryRallyState(date=pivotal_state.date.strftime('%Y-%m-%d'), price=pivotal_state.price, symbol=stock_id.symbol, prev_state=pivotal_state.prev_state, \
													 upward_trend=pivotal_state.upward_trend_point , downward_trend=pivotal_state.downward_trend_point, natural_reaction=pivotal_state.natural_reaction_point, \
													 natural_rally=pivotal_state.natural_rally_point, secondary_rally=pivotal_state.secondary_rally_point, secondary_reaction=pivotal_state.secondary_reaction_point)
				elif pivotal_state.state == SECONDARY_REACTION_STATE:
					pivotal_state = SecondaryReactionState(date=pivotal_state.date.strftime('%Y-%m-%d'), price=pivotal_state.price, symbol=stock_id.symbol, prev_state=pivotal_state.prev_state, \
													 upward_trend=pivotal_state.upward_trend_point , downward_trend=pivotal_state.downward_trend_point, natural_reaction=pivotal_state.natural_reaction_point, \
													 natural_rally=pivotal_state.natural_rally_point, secondary_rally=pivotal_state.secondary_rally_point, secondary_reaction=pivotal_state.secondary_reaction_point)
				else:
					print ("update {0} pivotal error: can't find state".format(stock_id))
				for stock_price in stock_prices:
					if (stock_price.date != pivotal_state.date):
						pivotal_state = pivotal_state.next(stock_price.close_price, stock_price.date.strftime('%Y-%m-%d'))
						pivotal_state.save_to_db()
						# print ('update {0} pivotal state, there has {1} datas'.format(stock_id.symbol, cnt))
						cnt += 1
				if cnt != 11:
					print ('update {0} pivotal state, there has {1} datas'.format(stock_id.symbol, cnt))
	lastDate = PivotalPoint.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = PivotalPoint.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='kp', last_update_date = datetime.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " pivotal point in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(lastDateDataCnt) + ' data in ' + lastDate.strftime("%Y-%m-%d")})

	return HttpResponse(json_obj, content_type="application/json")

def csv_test(request):
	with open('output.csv', 'w', newline='') as csvfile:
	# 建立 CSV 檔寫入器
		writer = csv.writer(csvfile)
	# 寫入一列資料
		writer.writerow(['姓名', '身高', '體重'])

	# 寫入另外幾列資料
		writer.writerow(['令狐沖', 175, 60])
		writer.writerow(['岳靈珊', 165, 57])
	return HttpResponse('download_test')

def download_keypoint(request):
	start_date = date(2016, 1, 1)
	pivotal_point = PivotalPoint.objects.filter(date__gte=start_date)
	sample_points = pivotal_point.filter(symbol='2330').order_by('date')
	encode = request.GET.get('encode', 'big5')

	response = HttpResponse(content_type='text/csv')
	today = datetime.today()
	last_monday = today - timedelta(days=today.weekday())
	filename = last_monday.strftime('%Y%m%d') + '_keypoint.csv'
	#filename = '/Users/vanhong/vk/test.csv'
	response['Content-Disposition'] = 'attachment; filename=' + filename

	writer = csv.writer(response, delimiter=',', quotechar='"')
	header = ['StockID','Name', 'Type']
	for p in sample_points:
		header.append(p.date)
	header.append('current')
	writer.writerow([x for x in header])
	#stock_ids = ['2610','2618','2612','2606','2208',
	#		'2330','6286','2337','3041','2458',
	#		'5483','3556',
	#		'2353','2324','3231','2382','2376',
	#		'2357','4938','2395','3022','6206',
	#		'2474','2387','6121','8210','3611',
	#		'2308','2420','2457','2327','2428',
	#		'6269','2383','3044','3037','2462',
	#		'6224','6279','3299','8042','8091',
	#		'3390','2317','6192','6146','3552',
	#		'3563','2393','6278','2486','2374',
	#		'5392','3454','3615','6231','5209',
	#		'3546','5478','2412','3045','4904',
	#		'2450','2345','2455','5388','3068',
	#		'3234','6143','6263','3702','3010',
	#		'6281','1535','1521','1525','1531',
	#		'4526','4532','8374','1580','6122',
	#		'1101','1102','1301','1303','1304',
	#		'1308','1326','1307','1325','6508',
	#		'1723','1710','1704','4725','1742',
	#		'2103','2105','2106','2108','6505',
	#		'6184','9904','9939','9925','9917',
	#		'9921','9914','9941','9924','5312',
	#		'1216','1201','1227','1232','1233',
	#		'1231','4205','1402','1477','1476',
	#		'2207','2548','5522','2820','2881','2886','2449','1452','6202', '6449', '3105',
	#		'2399', '2421']
	#stockids = WatchList.objects.values_list('symbol', flat=True)
	#stock_ids = StockId.objects.filter(symbol__in=stockids).order_by('company_type', 'symbol').values_list('symbol', flat=True)
	season_date = today - timedelta(days=120)
	stockids = WatchList.objects.filter(Q(user='vk')|Q(user='wawa')|Q(date__gte=season_date)).values_list('symbol', flat=True)
	#query = reduce(operator.and_, (Q(symbol__contains=item) for item in stockids))
	stock_ids = StockId.objects.filter(symbol__in=stockids).order_by('company_type', 'symbol').values_list('symbol', flat=True)
	
	for stock_id in stock_ids:
		if (StockId.objects.filter(symbol__contains=stock_id)):
			stockId = StockId.objects.get(symbol=stock_id)
			prev_point_state = ''
			body = [stock_id]
			body.append(stockId.name)
			body.append(stockId.company_type)
			points = pivotal_point.filter(symbol=stock_id).order_by('date')
			if (points.count() < sample_points.count()):
				for i in range(sample_points.count() - points.count()):
					body.append('-')
			for p in points:
				if (p.state != prev_point_state):
					body.append(str(p.price) + u'_' + p.state)
				else:
					body.append(str(p.price))
				prev_point_state = p.state
			body.append(p.state)
			writer.writerow([x for x in body])
	return response
