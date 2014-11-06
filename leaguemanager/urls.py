from django.conf.urls import patterns, url

from leaguemanager import views





urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^player/(?P<player_id>\d+)/$', views.player, name='player'),
	url(r'^league/(?P<league_id>\d+)/$', views.league, name='league'),
	url(r'^season/(?P<season_id>\d+)/$', views.season, name='season'),
    url(r'^add_player/$', views.add_player, name='add_player'),
    url(r'^add_member/(?P<league_id>\d+)/$', views.add_member, name='add_member'),
    url(r'^add_scoresheet/(?P<season_id>\d+)/$', views.add_scoresheet, name='add_scoresheet'),
    url(r'^edit_game/(?P<game_id>\d+)/$', views.edit_game, name='edit_game'),
    url(r'^add_season/(?P<league_id>\d+)/$', views.add_season, name='add_season'),
    url(r'^add_food/(?P<season_id>\d+)/$', views.add_food, name='add_food'),
)