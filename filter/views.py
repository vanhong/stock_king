from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from django.db.models import Count
import datetime
from django.views.decorators.csrf import csrf_exempt
from stocks.models import *
from financial.models import *
from core.util import *
from django.db.models import Avg
from django.db import connection
import pdb

# Create your views here.
def filter(request):
	return render(request, 'filter/index.html')

@csrf_exempt
def start_filter(request):
	try:
		request_date = request.POST['date']
		str_year, str_month, str_day = request_date.split('-')
		year = int(str_year)
		month = int(str_month)
		day =  int(str_day)
		date = datetime.date(year, month, day)
	except:
		date = datetime.date.today()
	conditions = {}
	for key, value in request.POST.items():
		if '-' in key:
			keySplit = key.split('-')
			condition = keySplit[0]
			para = keySplit[1]
			if condition in conditions.keys():
				conditions[condition][para] = value
			else:
				conditions[condition] = {para:value}
	filter_list = []
	for key, value in conditions.items():
		if key == 'm_revenue_yoy':
			update_lists = query_revenue_ann_growth_rate(int(value['cnt']), int(value['matchcnt']), 
			'gte', value['value'], 'month', date)
			filter_list.append(update_lists)
		elif key == 'm_revenue_avg_yoy':
			update_lists = query_revenug_avg_growth_rete(int(value['cnt']), value['value'], 'month', date)
			filter_list.append(update_lists)
		elif key == 's_revenue_yoy':
			update_lists = query_revenue_ann_growth_rate(int(value['cnt']), int(value['matchcnt']), 
			'gte', value['value'], 'season', date)
			filter_list.append(update_lists)
		elif key == 's_revenue_avg_yoy':
			update_lists = query_revenug_avg_growth_rete(int(value['cnt']), value['value'], 'season', date)
			filter_list.append(update_lists)
		elif key == 'opm_s':
			update_lists = query_financial_ratio_test(int(value['cnt']), value['value'], 'operating_profit_margin', 'season', date)
			filter_list.append(update_lists)
		elif key == 'gpm_s':
			update_lists = query_financial_ratio_test(int(value['cnt']), value['value'], 'gross_profit_margin', 'season', date)
			filter_list.append(update_lists)

	filterIntersection = []
	if len(filter_list) == 1:
		filterIntersection = filter_list[0]
	elif len(filter_list) >= 2:
		filterIntersection = filter_list[0]
		if len(filter_list) > 2:
			for i in range(2, len(filter_list)):
				filterIntersection = list(set(filterIntersection).intersection(set(filter_list[i])))
	new_list = sorted(filterIntersection)
	results_dic = {}
	header = ResultObj()
	header.name = 'Name'
	header.stockid = 'Symbol'
	header.company_type = 'Type'
	results_dic['0000'] = header
	for item in new_list:
		if StockId.objects.filter(symbol=item):
			resultObj = ResultObj()
			stockid = StockId.objects.get(symbol=item)
			resultObj.name = stockid.name
			resultObj.stockid = stockid.symbol
			resultObj.company_type = stockid.company_type
			results_dic[item] = resultObj

	context = {"results": results_dic}
	return render_to_response('filter/filter_result.html', 
		{'results':results_dic.items()})
	#return render(request, 'filter/filter_result.html', context)
	#return render_to_response(
	#	'filter/filter_result.html',{
	#	"results": results_dic},
	#	context_instance = RequestContext(request))

class ResultObj():
	def setName(self, name):
		self.name = name

#過去cnt個月內matchcnt個月營收年增率大於小於
def query_revenue_ann_growth_rate(cnt, matchcnt, overunder, growth_rate, reveneu_type, date):
	strDate = 'data_date'
	strSymbol = 'symbol'
	filter_date = date_to_revenue_date(date.year, date.month, date.day, reveneu_type)
	if reveneu_type == 'month':
		model = MonthRevenue
		startDate = month_minus(filter_date, -cnt + 1)
	elif reveneu_type == 'season':
		model = SeasonRevenue
		startDate = month_minus(filter_date, -(cnt-1) * 3)
	else:
		return None
	kwargs = {
		'{0}__{1}'.format('year_growth_rate', overunder):growth_rate,
		'{0}__{1}'.format(strDate, 'gte'):startDate,
		'{0}__{1}'.format(strDate, 'lte'):filter_date,
	} 
	lists = model.objects.values(strSymbol).filter(**kwargs).\
			annotate(symbol_count=Count(strSymbol)).filter(symbol_count__gte=matchcnt).values_list(strSymbol, flat=True)
	return lists

#過去cnt內營收平均年增率大於
def query_revenug_avg_growth_rete(cnt, growth_rate, reveneu_type, date):
	strDate = 'data_date'
	strSymbol = 'symbol'
	filter_date = date_to_revenue_date(date.year, date.month, date.day, reveneu_type)
	if reveneu_type == 'month':
		model = MonthRevenue
		startDate = month_minus(filter_date, -cnt + 1)
	elif reveneu_type == 'season':
		model = SeasonRevenue
		startDate = month_minus(filter_date, -(cnt-1) * 3)
	else:
		return None
	kwargs1 = {
		'{0}__{1}'.format(strDate, 'gte'):startDate,
		'{0}__{1}'.format(strDate, 'lte'):filter_date,
	}
	kwargs2 = {
		'{0}__{1}'.format('field_avg', 'gte'):growth_rate,
	}
	lists = model.objects.values(strSymbol).filter(**kwargs1).\
			annotate(symbol_count=Count(strSymbol)).filter(symbol_count=cnt).\
			annotate(field_avg=Avg('year_growth_rate')).\
			filter(**kwargs2).values_list(strSymbol, flat=True)
	return lists

#連續幾季(年)財務比率
def query_financial_ratio(cnt, ratio_value, field, time_type, date):
	strDate = 'data_date'
	strSymbol = 'symbol'
	filter_date = date_to_financial_date(date.year, date.month, date.day, time_type)
	if time_type == 'season':
		model = SeasonFinancialRatio
		dates = model.objects.filter(data_date__lte=filter_date).values(strDate).distinct().order_by('-'+strDate)[:cnt]
		startDate = dates[len(dates)-1][strDate]
	elif time_type == 'year':
		model = YearFinancialRatio
		dates = model.objects.filter(data_date__lte=filter_date).values(strDate).distinct().order_by('-'+strDate)[:cnt]
		startDate = dates[len(dates)-1][strDate]
	kwargs = {
		'{0}__{1}'.format(field, 'gte'):ratio_value,
		'{0}__{1}'.format(strDate, 'gte'):startDate,
		'{0}__{1}'.format(strDate, 'lte'):filter_date,
	}
	lists = model.objects.values(strSymbol).filter(**kwargs)
			#annotate(symbol_count=Count('symbol')).filter(symbol_count=cnt).\
			#values_list(strSymbol, flat=True)
	return lists

def query_financial_ratio_test(cnt, ratio_value, field, time_type, date):
	strDate = 'data_date'
	strSymbol = 'symbol'
	filter_date = date_to_financial_date(date.year, date.month, date.day, time_type)
	filter_date_str = '\''+filter_date.strftime('%Y-%m-%d')+'\''
	if time_type == 'season':
		model = 'stock_king.financial_seasonfinancialratio'
		dates = SeasonFinancialRatio.objects.filter(data_date__lte=filter_date).values(strDate).distinct().order_by('-'+strDate)[:cnt]
		startDate = dates[len(dates)-1][strDate]
	elif time_type == 'year':
		model = 'stock_king.financial_yearfinancialratio'
		dates = YearFinancialRatio.objects.filter(data_date__lte=filter_date).values(strDate).distinct().order_by('-'+strDate)[:cnt]
		startDate = dates[len(dates)-1][strDate]
	startDate_str = '\''+startDate.strftime('%Y-%m-%d')+'\''
	cursor = connection.cursor()
	query_str = ('SELECT symbol FROM ' + model + 
				 ' where data_date>=' + startDate_str + ' and data_date<=' +
				 filter_date_str + ' and ' +
				 field + '>' + ratio_value + ' group by symbol having count(symbol)=' + str(cnt))
	cursor.execute(query_str)
	cursor_lists = cursor.fetchall()
	lists = []
	for symbol in cursor_lists:
		lists.append(symbol[0])
	return lists

def test2():
	lists = query_revenue_ann_growth_rate(3, 3, 'gte', 30, 'month', '2017-12-01')
	return None
