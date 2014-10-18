from django.http import HttpResponse
from django.shortcuts import render

from django import template

from leaguemanager.models import Player, League, Season

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

def add_player(request):
    other = 'GET'
    if request.method == 'POST':
        name = request.POST['name']
        try:
            p = Player.objects.get(name=name)
            other = "POST: Player %s already exists!" % name
        except Player.DoesNotExist:
            first = request.POST['first']
            last = request.POST['last']
            email = request.POST['email']
            favorite = request.POST['favorite']
            p = Player(name=name, first_name=first, last_name=last, email_address=email, favorite_faction=favorite)
            p.save()
            other = "POST: Player %s was saved." % name 
    
    player_list = Player.objects.all()

    context = {'player_list': player_list, 'other': other}
    return render(request, 'leaguemanager/add_player.html', context)

def season2(request, season_id):
    season2 = Season.objects.get(id=season_id)
    player_list = season2.league.members.all()
    ps = {p.name: p.score(season2) for p in player_list}
    context = {
        # The .get_score_for_season method doesn't, and probably shouldn't,
        # exist - substitute your own logic here.
        'players_and_scores': ps
    }

    return render(request, 'leaguemanager/season2.html', context)


