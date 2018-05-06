from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^update_wawa_growth_power/$', views.update_wawa_growth_power, name='update_wawa_growth_power'),
	url(r'^update_vk_growth_power/$', views.update_vk_growth_power, name='update_vk_growth_power'),
	url(r'^update_avg_pe/$', views.update_avg_pe, name='update_avg_pe'),
]