from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^show_season_income_statement/$', views.show_season_income_statement, name='show_season_income_statement'),
	url(r'^update_season_income_statement/$', views.update_season_income_statement, name='update_season_income_statement'),
	url(r'^update_year_income_statement/$', views.update_year_income_statement, name='update_year_income_statement'),
	url(r'^show_season_balance_sheet/$', views.show_season_balance_sheet, name='show_season_balance_sheet'),
	url(r'^update_season_balance_sheet/$', views.update_season_balance_sheet, name='update_season_balance_sheet'),
	url(r'^show_season_cashflow_statement/$', views.show_season_cashflow_statement, name='show_season_cashflow_statement'),
	url(r'^update_season_cashflow_statement/$', views.update_season_cashflow_statement, name='update_season_cashflow_statement'),
	url(r'^update_season_financial_ratio/$', views.update_season_financial_ratio, name='update_season_financial_ratio'),
	url(r'^update_year_cashflow_statement/$', views.update_year_cashflow_statement, name='update_year_cashflow_statement'),
	url(r'^update_year_financial_ratio/$', views.update_year_financial_ratio, name='update_year_financial_ratio'),
	url(r'^update_data_date/$', views.update_data_date, name='update_data_date'),
]