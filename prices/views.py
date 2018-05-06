from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max
import urllib
import pdb
from decimal import Decimal
from datetime import *
from datetime import timedelta
from stocks.models import StockId
from prices.models import WeekPrice, PivotalPoint
from prices.pivotal_state import *
from stocks.models import UpdateManagement
import json

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
	lastDate = WeekPrice.objects.all().aggregate(Max('date'))['date__max']
	lastDateDataCnt = WeekPrice.objects.filter(date=lastDate).count()
	updateManagement = UpdateManagement(name='wp', last_update_date = datetime.today(),
										last_data_date = lastDate, 
										notes = "There is " + str(lastDateDataCnt) + " week price in " + lastDate.strftime("%Y-%m-%d"))
	updateManagement.save()
	json_obj = json.dumps({'dataDate': lastDate.strftime("%Y-%m-%d"), 'notes': 'update ' + str(lastDateDataCnt) + ' data in ' + lastDate.strftime("%Y-%m-%d")})

	return HttpResponse(json_obj, content_type="application/json")

def update_pivotal_state(request):
	stock_ids = StockId.objects.all()
	for stock_id in stock_ids:
		cnt = 0
		pivotal_point_count = PivotalPoint.objects.filter(symbol=stock_id.symbol).count()
		print("start update {0} pivotal".format(stock_id))
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
	return HttpResponse('update pivotal state')


