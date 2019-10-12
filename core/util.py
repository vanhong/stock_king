#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

def season_to_date(year, season):
	if season == 1:
		return datetime.date(year, 1, 1)
	elif season == 2:
		return datetime.date(year, 4, 1)
	elif season == 3:
		return datetime.date(year, 7, 1)
	elif season == 4:
		return datetime.date(year, 10, 1)

def month_minus(date, delta):
	m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
	if not m: m = 12
	d = min(date.day, [31,
		29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
	return date.replace(day=d,month=m, year=y)

def revenue_date_to_data_date(year, month):
	if month == 12:
		return datetime.date(year+1, 1, 10)
	else:
		return datetime.date(year, month+1, 10)

def financial_date_to_data_date(year, season):
	if season == 1:
		return datetime.date(year, 5, 15)
	elif season == 2:
		return datetime.date(year, 8, 14)
	elif season == 3:
		return datetime.date(year, 11, 14)
	elif season == 4:
		return datetime.date(year+1, 3, 31)

def date_to_revenue_date(year, month, day, revenue_type):
	if revenue_type == 'month':
		if day < 10:
			if month == 1:
				return datetime.date(year-1, 12, 10)
			else:
				return datetime.date(year, month-1, 10)
		else:
			return datetime.date(year, month , 10)
	elif revenue_type == 'season':
		if month >= 10:
			if day < 10:
				return datetime.date(year, 7, 10)
			else:
				return datetime.date(year, 10, 10)
		elif month >= 7:
			if day < 10:
				return datetime.date(year, 4, 10)
			else:
				return datetime.date(year, 7, 10)
		elif month >=4:
			if day < 10:
				return datetime.date(year, 1, 10)
			else:
				return datetime.date(year, 4, 10)
		elif month >=1:
			if day < 10:
				return datetime.date(year-1, 10, 10)
			else:
				return datetime.date(year, 1, 10)

def date_to_financial_date(year, month, day, financial_type):
	if financial_type == 'season':
		if month >= 12:
			return datetime.date(year, 11, 14)
		elif month >= 11:
			if day >= 14:
				return datetime.date(year, 11, 14)
			else:
				return datetime.date(year, 8, 14)
		elif month >=9:
			return datetime.date(year, 8, 14)
		elif month >=8:
			if day >= 14:
				return datetime.date(year, 8, 14)
			else:
				return datetime.date(year, 5, 15)
		elif month >= 6:
			return datetime.date(year, 5, 15)
		elif month >= 5:
			if day >= 15:
				return datetime.date(year, 5, 15)
			else:
				return datetime.date(year, 3, 31)
		elif month >= 4:
			return datetime.date(year, 3, 31)
		elif month >= 3:
			if day >= 31:
				return datetime.date(year, 3, 31)
			else:
				return datetime.date(year-1, 11, 14)
		else:
			return datetime.date(year-1, 11, 14)



