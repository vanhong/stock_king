from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.context import RequestContext
from django.db.models import Count
import datetime
from django.views.decorators.csrf import csrf_exempt
from stocks.models import *
from financial.models import *
from prices.models import *
from core.util import *
from django.db.models import Avg, Sum
from django.db import connection
import pdb

# Create your views here.
def filter(request):
	return render(request, 'filter/index.html')

@csrf_exempt
def start_filter(request):
	saveid = False
	try:
		request_date = request.POST['date']
		str_year, str_month, str_day = request_date.split('-')
		year = int(str_year)
		month = int(str_month)
		day =  int(str_day)
		date = datetime.date(year, month, day)
		if request.POST['saveid'] == 'true':
			saveid = True
		else:
			saveid = False
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
			update_lists = query_revenue_avg_growth_rete(int(value['cnt']), value['value'], 'month', date)
			filter_list.append(update_lists)
		elif key == 's_revenue_yoy':
			update_lists = query_revenue_ann_growth_rate(int(value['cnt']), int(value['matchcnt']), 
			'gte', value['value'], 'season', date)
			filter_list.append(update_lists)
		elif key == 's_revenue_avg_yoy':
			update_lists = query_revenue_avg_growth_rete(int(value['cnt']), value['value'], 'season', date)
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
		filterIntersection = list(set(filter_list[0]).intersection(set(filter_list[1])))
		if len(filter_list) > 2:
			for i in range(2, len(filter_list)):
				filterIntersection = list(set(filterIntersection).intersection(set(filter_list[i])))
	new_list = sorted(filterIntersection)
	results_dic = {}
	header = ResultObj()
	header.name = 'Name'
	header.stockid = 'Symbol'
	header.company_type = 'Type'
	header.price = '當下股價'
	header.eps = 'EPS'
	header.pe = 'PE'
	header.revenueGrowth = '月營收年增率'
	header.accRevenueGrowth = '累積營收年增率'
	header.opm_s = '季營益率'
	header.npm_s = '季淨利率'
	header.opm_s_yoy = '季營益率YOY'
	header.eps_s_yoy = '季EPS_YOY'
	header.dividend_con = '連續現金股利年數'
	header.quick_ratio = '速動比'
	header.three_twelve_revenue = '3個月營收avg/12個月營收avg'
	header.estimate_revenue_yoy = '預估下個月營收年增率'
	header.three_free_cashflow = '近3年自由現金流'
	header.opm_max_min = '近8季盈益率max/min'
	results_dic['0000'] = header
	for item in new_list:
		if StockId.objects.filter(symbol=item):
			resultObj = ResultObj()
			data_date = date_to_revenue_date(date.year, date.month, date.day, 'month')
			revenue_date = MonthRevenue.objects.filter(data_date=data_date)[0].date
			stockid = StockId.objects.get(symbol=item)
			resultObj.name = stockid.name
			resultObj.stockid = stockid.symbol
			resultObj.company_type = stockid.company_type
			resultObj.revenueGrowth = MonthRevenue.objects.filter(symbol=item, data_date__lte=data_date).order_by('-data_date')[0].year_growth_rate
			resultObj.accRevenueGrowth = MonthRevenue.objects.filter(symbol=item, data_date__lte=data_date).order_by('-data_date')[0].acc_year_growth_rate
			seasonFinancialRatios = SeasonFinancialRatio.objects.filter(symbol=item).order_by('-date')
			resultObj.opm_s = seasonFinancialRatios[0].operating_profit_margin
			resultObj.npm_s = seasonFinancialRatios[0].net_profit_margin_before_tax
			resultObj.quick_ratio = seasonFinancialRatios[0].quick_ratio
			data_date_2month = month_minus(data_date, -2)
			data_date_11month = month_minus(data_date, -11)
			near_3_month_revenue = MonthRevenue.objects.filter(symbol=item, data_date__lte=data_date, data_date__gte=data_date_2month)
			near_12_month_revenue = MonthRevenue.objects.filter(symbol=item, data_date__lte=data_date, data_date__gte=data_date_11month)
			if(near_3_month_revenue.count() == 3 and near_12_month_revenue.count()==12):
				three_month = near_3_month_revenue.aggregate(Avg('revenue'))['revenue__avg']
				twelve_month = near_12_month_revenue.aggregate(Avg('revenue'))['revenue__avg']
				resultObj.three_twelve_revenue = "{0:.1%}".format((three_month/twelve_month)-1)
			else:
				resultObj.three_twelve_revenue = 'NaN'
			try:
				this_month_revenue = MonthRevenue.objects.filter(symbol=item, data_date__lte=data_date).order_by('-data_date')[0].revenue
				last_eleven_month_revenue = MonthRevenue.objects.filter(symbol=item, data_date__lte=data_date).order_by('-data_date')[11].revenue
				resultObj.estimate_revenue_yoy = "{0:.1%}".format(this_month_revenue/last_eleven_month_revenue-1)
			except:
				resultObj.estimate_revenue_yoy = 'NaN'
			if (seasonFinancialRatios.count() >= 5):
				try:
					lastYear_opms = seasonFinancialRatios[4].operating_profit_margin
					resultObj.opm_s_yoy = "{0:.1%}".format((resultObj.opm_s / lastYear_opms)-1)
				except:
					resultObj.opm_s_yoy = 'NaN'
				try:
					lastYear_eps = seasonFinancialRatios[4].earnings_per_share
					eps = seasonFinancialRatios[0].earnings_per_share
					resultObj.eps_s_yoy = "{0:.1%}".format((eps / lastYear_eps)-1)
				except:
					resultObj.eps_s_yoy = 'NaN'
				try:
					resultObj.eps = seasonFinancialRatios[0].earnings_per_share + seasonFinancialRatios[1].earnings_per_share + \
									seasonFinancialRatios[2].earnings_per_share + seasonFinancialRatios[3].earnings_per_share
				except:
					resultObj.eps = 'NaN'
			else:
				resultObj.opm_s_yoy = 'NaN'
				resultObj.eps_s_yoy = 'NaN'
				resultObj.eps = 'NaN'
			try:
				recent8SFR = SeasonFinancialRatio.objects.filter(symbol=item).order_by('-date')[:8]
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
				resultObj.opm_max_min = "{0:.1%}".format((max_opm / min_opm)-1)
			except:
				resultObj.opm_max_min = 'NaN'
			
			dividends = Dividend.objects.filter(symbol=item).order_by('-date')
			dividend_con = 0
			if dividends.count() > 0:
				year = dividends[0].year + 1
			resultObj.dividend_con = dividend_con
			for dividend in dividends:
				try:
					if(dividend.cash_dividends > 0 and dividend.year == year-1):
						year = dividend.year
						dividend_con += 1
						resultObj.dividend_con = dividend_con
					else:
						resultObj.dividend_con = dividend_con
						break
				except:
					resultObj.dividend_con = dividend_con
			decimalPe = 0
			price = WeekPrice.objects.filter(symbol=item).order_by('-date')[0]
			resultObj.price = price.close_price
			if (seasonFinancialRatios.count() > 3):
				try:
					eps = seasonFinancialRatios[0].earnings_per_share +\
						seasonFinancialRatios[1].earnings_per_share +\
						seasonFinancialRatios[2].earnings_per_share +\
						seasonFinancialRatios[3].earnings_per_share
					decimalPe = (price.close_price / eps)
					resultObj.pe = '{0:.2f}'.format(decimalPe)
				except:
					resultObj.pe = 'NaN'
			else:
				resultObj.pe = 'NaN'
			yearCashflow = YearCashflowStatement.objects.filter(symbol=item).order_by('-date')
			if(yearCashflow.count()>=3):
				resultObj.three_free_cashflow = yearCashflow[0].net_cash_flows_from_used_in_operating_activities +\
				yearCashflow[1].net_cash_flows_from_used_in_operating_activities +\
				yearCashflow[2].net_cash_flows_from_used_in_operating_activities +\
				yearCashflow[0].net_cash_flows_from_used_in_investing_activities +\
				yearCashflow[1].net_cash_flows_from_used_in_investing_activities +\
				yearCashflow[2].net_cash_flows_from_used_in_investing_activities
			else:
				resultObj.three_free_cashflow = 'NaN'
			results_dic[item] = resultObj
		if saveid:
			if not WatchList.objects.filter(symbol=item, user='pick', date=revenue_date):
				watchlist = WatchList()
				watchlist.surrogate_key = 'pick_' + revenue_date.strftime('%Y-%m-%d') + '_' + item
				watchlist.user = 'pick'
				watchlist.symbol = item
				watchlist.rank = -1
				watchlist.date = revenue_date
				watchlist.save()
	context = {"results": results_dic.items()}
	return render(request, 'filter/filter_result.html', context)
	#return render_to_response('filter/filter_result.html', 
	#	{'results':results_dic.items()})
	#return render(request, 'filter/filter_result.html', context)
	#return render_to_response(
	#	'filter/filter_result.html',{
	#	"results": results_dic},
	#	context_instance = RequestContext(request))

class ResultObj():
	def setName(self, name):
		self.name = name

#過去cnt個月內matchcnt個月營收年增率大於小於
def query_revenue_ann_growth_rate(cnt, matchcnt, overunder, growth_rate, revenue_type, date):
	strDate = 'data_date'
	strSymbol = 'symbol'
	filter_date = date_to_revenue_date(date.year, date.month, date.day, revenue_type)
	if revenue_type == 'month':
		model = MonthRevenue
		startDate = month_minus(filter_date, -cnt + 1)
	elif revenue_type == 'season':
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
def query_revenue_avg_growth_rete(cnt, growth_rate, revenue_type, date):
	strDate = 'data_date'
	strSymbol = 'symbol'
	filter_date = date_to_revenue_date(date.year, date.month, date.day, revenue_type)
	if revenue_type == 'month':
		model = MonthRevenue
		startDate = month_minus(filter_date, -cnt + 1)
	elif revenue_type == 'season':
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

#連續幾季(年)財務比率(有錯誤)
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

#自己寫的正確版
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
				 field + '>' + ratio_value + ' group by symbol having count(symbol)>=' + str(cnt))
	cursor.execute(query_str)
	cursor_lists = cursor.fetchall()
	lists = []
	for symbol in cursor_lists:
		lists.append(symbol[0])
	return lists

def test2():
	lists = query_revenue_ann_growth_rate(3, 3, 'gte', 30, 'month', '2017-12-01')
	return None
