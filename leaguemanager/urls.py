from django.conf.urls import patterns, url

from leaguemanager import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^player/(?P<player_id>\d+)/$', views.player, name='player'),
	url(r'^league/(?P<league_id>\d+)/$', views.league, name='league'),
	url(r'^season/(?P<season_id>\d+)/$', views.season, name='season'),
    url(r'^add_player/$', views.add_player, name='add_player'),
    url(r'^add_player2/$', views.add_player2, name='add_player2'), #something I'm testing
    url(r'^season2/(?P<season_id>\d+)/$', views.season2, name='season2'), #something I'm testing
)