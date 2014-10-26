from django.http import HttpResponse
from django.shortcuts import render

from django import template

from leaguemanager.models import Player, League, Season, Membership

def index(request):
	player_list = Player.objects.all()
	league_list = League.objects.all()
	context = {'player_list': player_list, 'league_list': league_list}
	return render(request, 'leaguemanager/index.html', context)

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


def player(request, player_id):
	return HttpResponse("You're looking at the player detail page for %s." % Player.objects.get(pk=player_id))

def league(request, league_id):
    comment = 'GET'
    league = League.objects.get(pk=league_id)
    members = league.members.all()
    seasons = league.season_set.all()
    all_players = Player.objects.all()
    
    context = {
        'league': league, 
        'members': members, 
        'seasons': seasons, 
        'all_players': all_players, 
        'comment': comment
    }
    return render(request, 'leaguemanager/league.html', context)

def add_member(request, league_id):
    comment = 'GET'
    league = League.objects.get(pk=league_id)
    if request.method == 'POST':
        comment = 'POST'
        pta = request.POST['player_to_add']
        if pta == '0':
            comment = 'POST: error, you must pick a player'
        else:
            pta = Player.objects.get(name=pta)
            try:
                m = Membership.objects.get(player=pta, league=league)
                comment = 'POST: %s is already a member' % pta
            except Membership.DoesNotExist:
                m = Membership(player=pta, league=league)
                m.save()
                comment = 'POST: %s is now a member.' % pta 
    members = league.members.all()
    all_players = Player.objects.all()

    context = {
        'league': league,
        'members': members,
        'all_players': all_players,
        'comment': comment
    }
    return render(request, 'leaguemanager/add_member.html', context)

    

def season(request, season_id):
    season = Season.objects.get(id=season_id)
    league = season.league
    players = league.members.all()
    ps = {p.name: p.score(season) for p in players}
    ps = sorted(ps.items(), key=lambda t: t[1], reverse=True)
    games = season.game_set.all()
    context = {
        'season': season, 
        'league': league,
        'players_and_scores': ps,
        'games': games,
    }
    return render(request, 'leaguemanager/season.html', context)

def add_scoresheet(request, season_id):
    comment = 'GET'
    if request.method == 'POST':
        comment = 'POST'

    season = Season.objects.get(id=season_id)
    league = season.league
    players = league.members.all()
    context = {
        'season': season,
        'league': league,
        'comment': comment,
        'players': players
    }
    return render(request, 'leaguemanager/add_scoresheet.html', context)
















# testing area

from django.forms import ModelForm

def add_player2(request):
    class PlayerForm(ModelForm):
        class Meta:
            model = Player
            fields = ['name', 'first_name', 'last_name', 'email_address', 'favorite_faction']
    form = PlayerForm()
    context = {'form': form}
    return render(request, 'leaguemanager/add_player2.html', context)


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


