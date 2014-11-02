from django.http import HttpResponse
from django.shortcuts import render

from django import template

from datetime import datetime

from leaguemanager.models import Player, League, Season, Membership, FoodBonus, Game
from leaguemanager.ID_lists import *





def index(request):
	player_list = Player.objects.all()
	league_list = League.objects.all()

	context = {
        'player_list': player_list, 
        'league_list': league_list,
    }
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

    context = {
        'player_list': player_list, 
        'other': other
    }
    return render(request, 'leaguemanager/add_player.html', context)    





def player(request, player_id):
    player = Player.objects.get(id=player_id)
    leagues = player.league_set.all()

    context = {
        'player': player,
        'leagues': leagues,
    }

    return render(request, 'leaguemanager/player.html', context)





def league(request, league_id):
    league = League.objects.get(pk=league_id)
    members = league.members.all()
    seasons = league.season_set.all()
    all_players = Player.objects.all()
    
    context = {
        'league': league, 
        'members': members, 
        'seasons': seasons, 
        'all_players': all_players, 
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

    members = sorted(league.members.all(), key=lambda x: x.name.lower())
    all_players = sorted(Player.objects.all(), key=lambda x: x.name.lower())

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
    players = season.participants
    ps = {p.name: p.score(season) for p in players}
    ps = sorted(ps.items(), key=lambda t: t[1], reverse=True)
    games = season.game_set.all()
    num_of_games = len(games)
    foodbonuses = season.foodbonus_set.all()
    num_of_fbs = len(foodbonuses)

    context = {
        'season': season, 
        'league': league,
        'players_and_scores': ps,
        'games': games,
        'num_of_games': num_of_games,
        'foodbonuses': foodbonuses,
        'num_of_fbs': num_of_fbs,
    }
    return render(request, 'leaguemanager/season.html', context)





def add_scoresheet(request, season_id):
    comment = ['GET']
    season = Season.objects.get(id=season_id)
    league = season.league
    players = league.members.all()
    corp_IDs = corp_ID_list()
    corp_IDs.pop(-1)
    runner_IDs = runner_ID_list()
    runner_IDs.pop(-1) 

    if request.method == 'POST':
        comment = ['POST', request.POST]
        try:
            date = request.POST['gamedate']
            date = datetime.strptime(date, '%m/%d/%Y').date()
        except ValueError:
            comment.append('invalid date')
            date = None
        
        if date:
            id1 = request.POST['player1']
            id2 = request.POST['player2']

            if id1 == id2:
                comment.append('You must choose different players.')
            else:
                player1 = Player.objects.get(id=request.POST['player1'])
                player2 = Player.objects.get(id=request.POST['player2'])

                # add food bonuses to the database  
                if request.POST['player_1_food'] == 'True':
                    try:
                        fb = FoodBonus.objects.get(player=player1, season=season, date=date)
                        comment.append('%s already exists!' % fb)
                    except FoodBonus.DoesNotExist:
                        fb = FoodBonus(player=player1, season=season, date=date)
                        fb.save()
                        comment.append('FoodBonus saved for %s on %s' % (player1, date))
                if request.POST['player_2_food'] == 'True':
                    try:
                        fb = FoodBonus.objects.get(player=player2, season=season, date=date)
                        comment.append('%s already exists!' % fb)
                    except FoodBonus.DoesNotExist:
                        fb = FoodBonus(player=player2, season=season, date=date)
                        fb.save()
                        comment.append('FoodBonus saved for %s on %s' % (player2, date))

                # save game 1
                outcome = request.POST['game1outcome']
                player1id = request.POST['player1game1id']
                player2id = request.POST['player2game1id']
                v1 = (outcome == 'notplayed')
                v2 = (player1id == '0')
                v3 = (player2id == '0')
                v4 = ((player1id in corp_IDs) and (player2id in corp_IDs))
                v5 = ((player1id in runner_IDs) and (player2id in runner_IDs))
                if v1 or v2 or v3 or v4 or v5:
                    comment.append('Game 1 was not played or invalid')
                else: 
                    comment.append('Game 1 valid')
                    if ((player1id in corp_IDs) and (player2id in runner_IDs)):
                        corp_player = player1
                        corp_id = player1id
                        runner_player = player2
                        runner_id = player2id
                        if outcome == 'player1agendavictory':
                            outcome = 'corp agenda victory'
                        if outcome == 'player2agendavictory':
                            outcome = 'runner agenda victory'
                    else:
                        corp_player = player2
                        corp_id = player2id
                        runner_player = player1
                        runner_id = player1id
                        if outcome == 'player1agendavictory':
                            outcome = 'runner agenda victory'
                        if outcome == 'player2agendavictory':
                            outcome = 'corp agenda victory'

                    g = Game(
                        season=season,
                        date=date,
                        outcome=outcome,
                        corp_player=corp_player,
                        runner_player=runner_player,
                        corp_ID=corp_id,
                        runner_ID=runner_id
                    )
                    g.save()
                    comment.append('Game 1 saved.')

                # save game 2
                outcome = request.POST['game2outcome']
                player1id = request.POST['player1game2id']
                player2id = request.POST['player2game2id']
                v1 = (outcome == 'notplayed')
                v2 = (player1id == '0')
                v3 = (player2id == '0')
                v4 = ((player1id in corp_IDs) and (player2id in corp_IDs))
                v5 = ((player1id in runner_IDs) and (player2id in runner_IDs))
                if v1 or v2 or v3 or v4 or v5:
                    comment.append('Game 2 was not played or invalid')
                else: 
                    comment.append('Game 2 valid')
                    if ((player1id in corp_IDs) and (player2id in runner_IDs)):
                        corp_player = player1
                        corp_id = player1id
                        runner_player = player2
                        runner_id = player2id
                        if outcome == 'player1agendavictory':
                            outcome = 'corp agenda victory'
                        if outcome == 'player2agendavictory':
                            outcome = 'runner agenda victory'
                    else:
                        corp_player = player2
                        corp_id = player2id
                        runner_player = player1
                        runner_id = player1id
                        if outcome == 'player1agendavictory':
                            outcome = 'runner agenda victory'
                        if outcome == 'player2agendavictory':
                            outcome = 'corp agenda victory'

                    g = Game(
                        season=season,
                        date=date,
                        outcome=outcome,
                        corp_player=corp_player,
                        runner_player=runner_player,
                        corp_ID=corp_id,
                        runner_ID=runner_id
                    )
                    g.save()
                    comment.append('Game 2 saved.')

                # save game 3
                outcome = request.POST['game3outcome']
                player1id = request.POST['player1game3id']
                player2id = request.POST['player2game3id']
                v1 = (outcome == 'notplayed')
                v2 = (player1id == '0')
                v3 = (player2id == '0')
                v4 = ((player1id in corp_IDs) and (player2id in corp_IDs))
                v5 = ((player1id in runner_IDs) and (player2id in runner_IDs))
                if v1 or v2 or v3 or v4 or v5:
                    comment.append('Game 3 was not played or invalid')
                else: 
                    comment.append('Game 3 valid')
                    if ((player1id in corp_IDs) and (player2id in runner_IDs)):
                        corp_player = player1
                        corp_id = player1id
                        runner_player = player2
                        runner_id = player2id
                        if outcome == 'player1agendavictory':
                            outcome = 'corp agenda victory'
                        if outcome == 'player2agendavictory':
                            outcome = 'runner agenda victory'
                    else:
                        corp_player = player2
                        corp_id = player2id
                        runner_player = player1
                        runner_id = player1id
                        if outcome == 'player1agendavictory':
                            outcome = 'runner agenda victory'
                        if outcome == 'player2agendavictory':
                            outcome = 'corp agenda victory'

                    g = Game(
                        season=season,
                        date=date,
                        outcome=outcome,
                        corp_player=corp_player,
                        runner_player=runner_player,
                        corp_ID=corp_id,
                        runner_ID=runner_id
                    )
                    g.save()
                    comment.append('Game 3 saved.')

                # save game 4
                outcome = request.POST['game4outcome']
                player1id = request.POST['player1game4id']
                player2id = request.POST['player2game4id']
                v1 = (outcome == 'notplayed')
                v2 = (player1id == '0')
                v3 = (player2id == '0')
                v4 = ((player1id in corp_IDs) and (player2id in corp_IDs))
                v5 = ((player1id in runner_IDs) and (player2id in runner_IDs))
                if v1 or v2 or v3 or v4 or v5:
                    comment.append('Game 4 was not played or invalid')
                else: 
                    comment.append('Game 4 valid')
                    if ((player1id in corp_IDs) and (player2id in runner_IDs)):
                        corp_player = player1
                        corp_id = player1id
                        runner_player = player2
                        runner_id = player2id
                        if outcome == 'player1agendavictory':
                            outcome = 'corp agenda victory'
                        if outcome == 'player2agendavictory':
                            outcome = 'runner agenda victory'
                    else:
                        corp_player = player2
                        corp_id = player2id
                        runner_player = player1
                        runner_id = player1id
                        if outcome == 'player1agendavictory':
                            outcome = 'runner agenda victory'
                        if outcome == 'player2agendavictory':
                            outcome = 'corp agenda victory'

                    g = Game(
                        season=season,
                        date=date,
                        outcome=outcome,
                        corp_player=corp_player,
                        runner_player=runner_player,
                        corp_ID=corp_id,
                        runner_ID=runner_id
                    )
                    g.save()
                    comment.append('Game 4 saved.')
    
    context = {
        'season': season,
        'league': league,
        'comment': comment,
        'players': players,
        'runner_IDs': runner_IDs,
        'corp_IDs': corp_IDs
    }
    return render(request, 'leaguemanager/add_scoresheet.html', context)





def edit_game(request, game_id):
    game = Game.objects.get(id=game_id)
    season = game.season
    league = season.league
    members = league.members.all()
    corp_IDs = corp_ID_list()
    corp_IDs.pop(-1)
    runner_IDs = runner_ID_list()
    runner_IDs.pop(-1)
    
    outcomelist = [
        'draw',
        'corp agenda victory',
        'runner agenda victory',
        'flatline',
        'mill'
    ]
    comment = 'GET'


    if request.method == 'POST':
        comment = request.POST
        if request.POST['action'] == 'update':
            try:
                newdate = request.POST['gamedate']
                newdate = datetime.strptime(newdate, '%m/%d/%Y').date()
            except ValueError:
                newdate = None
        
            if newdate:
                if not request.POST['corpplayer'] == request.POST['runnerplayer']:
                    game.date = newdate
                    game.corp_player = Player.objects.get(id=request.POST['corpplayer'])
                    game.corp_ID = request.POST['corpid']
                    game.runner_player = Player.objects.get(id=request.POST['runnerplayer'])
                    game.runner_ID = request.POST['runnerid']
                    game.outcome = request.POST['gameoutcome']
                    game.save()
        else:
            game.delete()
            
            context = {
                'game_id': game_id,
                'season': season,
                'league': league,
                'comment': comment
            }
            return render(request, 'leaguemanager/game_deleted.html', context)


    formatteddate = game.date.strftime('%m/%d/%Y')
    context = {
        'game': game,
        'season': season,
        'league': league,
        'members': members,
        'corp_IDs': corp_IDs,
        'runner_IDs': runner_IDs,
        'formatteddate': formatteddate,
        'outcomelist': outcomelist,
        'comment': comment,
    }
    return render(request, 'leaguemanager/edit_game.html', context)




## testing something!
## at this point seasontest is better than season



def seasontest(request, season_id):
    season = Season.objects.get(id=season_id)
    league = season.league
    games = season.game_set.all()
    num_of_games = len(games)
    parts = season.participants
    foodbonuses = season.foodbonus_set.all()
    num_of_fbs = len(foodbonuses)

    scores = {}
    attendence_dates = {}

    gametest = {}

    for player in parts:
        scores[player] = 0
        attendence_dates[player] = set([])

    for game in games:
        c = game.corp_player
        r = game.runner_player
        d = game.date
        scores[c] += 1
        scores[r] += 1
        attendence_dates[c].add(d)
        attendence_dates[r].add(d)
        if game.winning_player:
            scores[game.winning_player] += 1
        

    for fb in foodbonuses:
        attendence_dates[fb.player].add(fb.date)

    for player in parts:
        scores[player] += 5*len(attendence_dates[player])
        scores[player] += 5*len(player.foodbonus_set.filter(season=season))

    scores = sorted(scores.items(), key=lambda t: t[1], reverse=True)

    context = {
        'season': season,
        'league': league,
        'scores': scores,
        'attendence_dates': attendence_dates,
        'games': games,
        'num_of_games': num_of_games,
        'foodbonuses': foodbonuses,
        'num_of_fbs': num_of_fbs,
    }
    return render(request, 'leaguemanager/seasontest.html', context)