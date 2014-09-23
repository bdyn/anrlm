from django.conf.urls import patterns, url

from leaguemanager import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^player/(?P<player_id>\d+)/$', views.player, name='player'),
	url(r'^league/(?P<league_id>\d+)/$', views.league, name='league'),
)