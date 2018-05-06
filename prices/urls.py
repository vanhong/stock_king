from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^show_price/$', views.show_price, name='show_price'),
	url(r'^update_price/$', views.update_price, name='update_price'),
	url(r'^update_pivotal_state/$', views.update_pivotal_state, name='update_pivotal_state')
]