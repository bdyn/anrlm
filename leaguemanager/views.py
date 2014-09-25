from django.http import HttpResponse
from django.shortcuts import render

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

