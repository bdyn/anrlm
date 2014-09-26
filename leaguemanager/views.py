from django.http import HttpResponse
from django.shortcuts import render

from django import template

from leaguemanager.models import Player, League, Season, Scorecard

def index(request):
	player_list = Player.objects.all()
	league_list = League.objects.all()
	context = {'player_list': player_list, 'league_list': league_list}
	return render(request, 'leaguemanager/index.html', context)

def player(request, player_id):
	return HttpResponse("You're looking at the player detail page for %s." % Player.objects.get(pk=player_id))

def league(request, league_id):
	return HttpResponse("You're looking at the league detail page for %s." % League.objects.get(pk=league_id))

def season(request, season_id):
    return HttpResponse("You're looking at the season detail page for %s." % Season.objects.get(pk=season_id))

def season2(request, season_id):
    season2 = Season.objects.get(id=season_id)
    player_list = season2.league.members.all()

    context = {
        'player_list': player_list,
        'season2' : season2,
        # The .get_score_for_season method doesn't, and probably shouldn't,
        # exist - substitute your own logic here.
        'players_and_scores': {p.name: p.get_score_for_season(season2) for p in player_list},
    }

    return render(request, 'leaguemanager/season2.html', context)


