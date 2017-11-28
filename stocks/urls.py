from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^update_month_revenue/$', views.update_month_revenue, name='update_month_revenue'),
	url(r'^update_season_revenue/$', views.update_season_revenue, name='update_season_revenue'),
	url(r'^update_stockid/$', views.update_stockid, name='update_stockid'),
]