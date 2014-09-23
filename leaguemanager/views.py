from django.http import HttpResponse
from django.shortcuts import render

from leaguemanager.models import Player

def index(request):
	player_list = Player.objects.all()
	context = {'player_list': player_list}
	return render(request, 'leaguemanager/index.html', context)

def player(request, player_id):
	return HttpResponse("You're looking at the player detail page for %s." % Player.objects.get(pk=player_id))