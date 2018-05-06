from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^filter/$', views.filter, name='filter'),
	url(r'^start_filter/$', views.start_filter, name='start_filter'),
]