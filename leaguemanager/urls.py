from django.conf.urls import patterns, url

from leaguemanager import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
)