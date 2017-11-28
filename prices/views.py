from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max
import urllib
import pdb
from decimal import Decimal
from datetime import *
from datetime import timedelta
from stocks.models import StockId
from prices.models import WeekPrice

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
		if last_monday.date() == lastest_price_date['date__max']:
			continue
		url = 'http://jsjustweb.jihsun.com.tw/Z/ZC/ZCW/czkc1.djbcd?a=' + stockid.symbol + '&b=W&c=2880&E=1&ver=5'
		response = urllib.request.urlopen(url)
		datas = response.read().split()
		dates = datas[0].split(b',')
		opens = datas[1].split(b',')
		highs = datas[2].split(b',')
		lows = datas[3].split(b',')
		closes = datas[4].split(b',')
		volumes = datas[5].split(b',')
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
	return HttpResponse('update %d history price' % (symbol_cnt))


