from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^books$', views.home),
	url(r'^books/add$', views.addbook),
	url(r'^books/create$', views.createbook),
	url(r'^books/(?P<id>\d+)$', views.viewbook),
	url(r'^users/(?P<id>\d+)$', views.viewuser),
	url(r'^users/register$', views.register),
	url(r'^users/logout$', views.logout),
	url(r'^users/login$', views.login),	
	url(r'^books/(?P<id>\d+)/addreview$', views.addreview),
]