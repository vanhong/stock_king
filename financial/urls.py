from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^show_season_income_statement/$', views.show_season_income_statement, name='show_season_income_statement'),
	url(r'^update_season_income_statement/$', views.update_season_income_statement, name='update_season_income_statement'),
	url(r'^show_season_balance_sheet/$', views.show_season_balance_sheet, name='show_season_balance_sheet'),
]