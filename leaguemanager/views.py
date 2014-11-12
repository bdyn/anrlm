from django.http import HttpResponse
from django.shortcuts import render

from django import template

from datetime import datetime
from itertools import combinations, permutations

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
            p = Player(
                name=name,
                first_name=first,
                last_name=last,
                email_address=email,
                favorite_faction=favorite
            )
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











def add_scoresheet(request, season_id):
    comment = ['GET']
    season = Season.objects.get(id=season_id)
    league = season.league
    players = league.members.all().order_by('name')
    corp_IDs = corp_ID_list()
    corp_IDs.pop(-1)
    runner_IDs = runner_ID_list()
    runner_IDs.pop(-1) 

    if request.method == 'POST':
        comment = ['POST', request.POST]
        try:
            date = request.POST['gamedate']
            date = datetime.strptime(date, '%Y-%m-%d').date()
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
                newdate = datetime.strptime(newdate, '%Y-%m-%d').date()
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


    formatteddate = game.date.strftime('%Y-%m-%d')
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





def add_season(request, league_id):
    league = League.objects.get(pk=league_id)
    comment = 'GET'

    if request.method == 'POST':
        comment = request.POST
        seasonname = request.POST['seasonname']
        begindate = request.POST['begindate']
        enddate = request.POST['enddate']

        try:
            begindate = datetime.strptime(begindate, '%Y-%m-%d').date()
        except ValueError:
            comment = 'invalid begin date'
            begindate = None
        
        try:
            enddate = datetime.strptime(enddate, '%Y-%m-%d').date()
        except ValueError:
            comment = 'invalid end date'
            enddate = None

        if begindate and enddate and (begindate < enddate):
            try:
                s = Season.objects.get(name=seasonname)
                comment = 'There is already a season with that name.'
            except Season.DoesNotExist:
                s = Season(
                    name=seasonname,
                    begin_date=begindate,
                    end_date=enddate,
                    league=league
                )
                s.save()
                comment = 'New season saved!'
        else:
            comment = 'Error with your chosen dates.'   

    seasons = league.season_set.all()     

    context = {
        'league': league,
        'seasons': seasons,
        'comment': comment,
    }
    return render(request, 'leaguemanager/add_season.html', context)




def add_food(request, season_id):
    season = Season.objects.get(id=season_id)
    league = season.league
    comment = 'GET'
    members = league.members.all()

    if request.method == 'POST':
        comment = request.POST
        date = request.POST['date']
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            comment = 'invalid date'
            date = None

        if date:
            player = Player.objects.get(id=request.POST['player'])
            fb = FoodBonus(
                player=player,
                date=date,
                season=season
                )
            fb.save()
            comment = 'Food bonus saved for %s on %s.' % (player, date)  



    context = {
        'season': season,
        'league': league,
        'comment': comment,
        'members': members
    }
    return render(request, 'leaguemanager/add_food.html', context)




## testing something!
## at this point seasontest is better than season



def season(request, season_id):
    season = Season.objects.get(id=season_id)
    league = season.league
    games = season.game_set.all()
    num_of_games = len(games)
    parts = season.participants
    foodbonuses = season.foodbonus_set.all()
    num_of_fbs = len(foodbonuses)

    pairs = list(permutations(parts, 2))
    corp_IDs = corp_ID_list()
    runner_IDs = runner_ID_list()

    # define tallies
    dates = set([])

    total_corp_agenda_wins = 0
    total_runner_agenda_wins = 0
    total_draws = 0
    total_mills = 0
    total_flatlines = 0

    corp_ID_game_tally = {}
    corp_ID_AGwin_tally = {}
    corp_ID_flatline_tally = {}
    corp_ID_AGloss_tally = {}
    corp_ID_mill_tally = {}
    corp_ID_draw_tally = {}

    runner_ID_game_tally = {}
    runner_ID_AGwin_tally = {}
    runner_ID_mill_tally = {}
    runner_ID_AGloss_tally = {}
    runner_ID_flatline_tally = {}
    runner_ID_draw_tally = {}

    player_corp_game_tally = {}
    player_corp_agenda_win_tally = {}
    player_corp_agenda_loss_tally = {}
    player_corp_flatline_tally = {}
    player_corp_mill_tally = {}
    player_corp_draw_tally = {}
    player_runner_game_tally = {}
    player_runner_agenda_win_tally = {}
    player_runner_agenda_loss_tally = {}
    player_runner_flatline_tally = {}
    player_runner_mill_tally = {}
    player_runner_draw_tally = {}

    player_game_tally = {}
    player_win_tally = {}
    player_loss_tally = {}
    player_draw_tally = {}

    player_food_dates = {}
    player_food_dates_tally = {}
    player_dates = {}
    player_dates_tally = {}
    player_win_dates = {}

    pair_multiplicities = {}

    player_score = {}
    player_game_score = {}
    player_sos = {}



    # set tallies to zero or empty set
    for ID in corp_IDs:
        corp_ID_game_tally[ID] = 0
        corp_ID_AGwin_tally[ID] = 0
        corp_ID_flatline_tally[ID] = 0
        corp_ID_AGloss_tally[ID] = 0
        corp_ID_mill_tally[ID] = 0
        corp_ID_draw_tally[ID] = 0

    for ID in runner_IDs:
        runner_ID_game_tally[ID] = 0
        runner_ID_AGwin_tally[ID] = 0
        runner_ID_mill_tally[ID] = 0
        runner_ID_AGloss_tally[ID] = 0
        runner_ID_flatline_tally[ID] = 0
        runner_ID_draw_tally[ID] = 0

    for player in parts:
        player_corp_game_tally[player] = 0
        player_corp_agenda_win_tally[player] = 0
        player_corp_agenda_loss_tally[player] = 0
        player_corp_flatline_tally[player] = 0
        player_corp_mill_tally[player] = 0
        player_corp_draw_tally[player] = 0
        
        player_runner_game_tally[player] = 0
        player_runner_agenda_win_tally[player] = 0
        player_runner_agenda_loss_tally[player] = 0
        player_runner_flatline_tally[player] = 0
        player_runner_mill_tally[player] = 0
        player_runner_draw_tally[player] = 0
        
        player_game_tally[player] = 0
        player_win_tally[player] = 0
        player_loss_tally[player] = 0
        player_draw_tally[player] = 0

        player_dates[player] = set([]) # disregard multiplicities
        player_food_dates[player] = set([]) # disregard multiplicies
        player_dates_tally[player] = 0
        player_food_dates_tally[player] = 0
        player_win_dates[player] = [] # need to track multiplicities

        player_score[player] = 0
        player_game_score[player] = 0
        player_sos[player] = 0

    for pair in pairs:
        pair_multiplicities[pair] = 0


    # count tallies
    for game in games:
        corp = game.corp_player
        runner = game.runner_player
        corp_ID = game.corp_ID
        runner_ID = game.runner_ID
        outcome = game.outcome
        date = game.date

        dates.add(date)
        player_dates[corp].add(date)
        player_dates[runner].add(date)

        if game.winning_player:
            player_win_dates[game.winning_player].append(date)

        player_corp_game_tally[corp] += 1
        player_game_tally[corp] += 1
        player_runner_game_tally[runner] += 1
        player_game_tally[runner] += 1

        corp_ID_game_tally[corp_ID] += 1
        runner_ID_game_tally[runner_ID] += 1
        
        if outcome == 'draw':
            corp_ID_draw_tally[corp_ID] += 1
            runner_ID_draw_tally[runner_ID] += 1
            total_draws += 1
            player_corp_draw_tally[corp] += 1
            player_runner_draw_tally[runner] += 1
            player_draw_tally[corp] += 1
            player_draw_tally[runner] += 1
        elif outcome == 'corp agenda victory':
            corp_ID_AGwin_tally[corp_ID] += 1
            runner_ID_AGloss_tally[runner_ID] +=1
            total_corp_agenda_wins += 1
            player_corp_agenda_win_tally[corp] += 1
            player_runner_agenda_loss_tally[runner] += 1
            player_win_tally[corp] += 1
            player_loss_tally[runner] += 1
        elif outcome == 'runner agenda victory':
            corp_ID_AGloss_tally[corp_ID] += 1
            runner_ID_AGwin_tally[runner_ID] += 1
            total_runner_agenda_wins += 1
            player_corp_agenda_loss_tally[corp] += 1
            player_runner_agenda_win_tally[runner] += 1
            player_win_tally[runner] += 1
            player_loss_tally[corp] += 1
        elif outcome == 'flatline':
            corp_ID_flatline_tally[corp_ID] += 1
            runner_ID_flatline_tally[runner_ID] += 1
            total_flatlines += 1
            player_corp_flatline_tally[corp] += 1
            player_runner_flatline_tally[runner] += 1
            player_win_tally[corp] += 1
            player_loss_tally[runner] += 1
        else: # outcome == 'mill'
            corp_ID_mill_tally[corp_ID] += 1
            runner_ID_mill_tally[runner_ID] += 1
            total_mills += 1
            player_corp_mill_tally[corp] += 1
            player_runner_mill_tally[runner] += 1
            player_win_tally[runner] += 1
            player_loss_tally[corp] += 1
        
        pair_multiplicities[(corp, runner)] += 1
        pair_multiplicities[(runner, corp)] += 1


    for fb in foodbonuses:
        date = fb.date
        player = fb.player
        player_dates[player].add(date)
        player_food_dates[player].add(date)
        dates.add(date)

    for player in parts:
        player_dates_tally[player] = len(player_dates[player])
        player_food_dates_tally[player] = len(player_food_dates[player])
        
        player_game_score[player] += player_game_tally[player]
        for d in set(player_win_dates[player]):
            player_game_score[player] += min(player_win_dates[player].count(d), 5)

        player_score[player] += player_game_score[player]
        player_score[player] += 5*player_dates_tally[player]
        player_score[player] += 5*player_food_dates_tally[player]

    for player in parts:
        for other_player in parts:
            if not player == other_player:
                player_sos[player] += player_game_score[other_player]*pair_multiplicities[(player, other_player)]


    # process tallies for display
    dates = sorted(list(dates))

    corp_stats = [
        (
            ID,
            corp_ID_game_tally[ID],
            round(100.0*corp_ID_game_tally[ID]/num_of_games, 2) if num_of_games > 0 else 0.0,
            corp_ID_AGwin_tally[ID],
            round(100.0*corp_ID_AGwin_tally[ID]/corp_ID_game_tally[ID], 2) if corp_ID_game_tally[ID] > 0 else 0.0,
            corp_ID_flatline_tally[ID],
            round(100.0*corp_ID_flatline_tally[ID]/corp_ID_game_tally[ID], 2) if corp_ID_game_tally[ID] > 0 else 0.0,
            corp_ID_AGloss_tally[ID],
            round(100.0*corp_ID_AGloss_tally[ID]/corp_ID_game_tally[ID], 2) if corp_ID_game_tally[ID] > 0 else 0.0,
            corp_ID_mill_tally[ID],
            round(100.0*corp_ID_mill_tally[ID]/corp_ID_game_tally[ID], 2) if corp_ID_game_tally[ID] > 0 else 0.0,
            corp_ID_draw_tally[ID],
            round(100.0*corp_ID_draw_tally[ID]/corp_ID_game_tally[ID], 2) if corp_ID_game_tally[ID] > 0 else 0.0            
        )
        for ID in corp_IDs 
    ]
    corp_stats = [x for x in corp_stats if not x[1] == 0]
    corp_stats = sorted(corp_stats, key=lambda t: t[1], reverse=True)

    runner_stats = [
        (
            ID,
            runner_ID_game_tally[ID],
            round(100.0*runner_ID_game_tally[ID]/num_of_games, 2) if num_of_games > 0 else 0.0,
            runner_ID_AGwin_tally[ID],
            round(100.0*runner_ID_AGwin_tally[ID]/runner_ID_game_tally[ID], 2) if runner_ID_game_tally[ID] > 0 else 0.0,
            runner_ID_mill_tally[ID],
            round(100.0*runner_ID_mill_tally[ID]/runner_ID_game_tally[ID], 2) if runner_ID_game_tally[ID] > 0 else 0.0,
            runner_ID_AGloss_tally[ID],
            round(100.0*runner_ID_AGloss_tally[ID]/runner_ID_game_tally[ID], 2) if runner_ID_game_tally[ID] > 0 else 0.0,
            runner_ID_flatline_tally[ID],
            round(100.0*runner_ID_flatline_tally[ID]/runner_ID_game_tally[ID], 2) if runner_ID_game_tally[ID] > 0 else 0.0,
            runner_ID_draw_tally[ID],
            round(100.0*runner_ID_draw_tally[ID]/runner_ID_game_tally[ID], 2) if runner_ID_game_tally[ID] > 0 else 0.0            
        )
        for ID in runner_IDs
    ]
    runner_stats = [x for x in runner_stats if not x[1] == 0]
    runner_stats = sorted(runner_stats, key=lambda t: t[1], reverse=True)

    game_stats = [
        total_corp_agenda_wins,
        round(100.0*total_corp_agenda_wins/num_of_games, 2) if num_of_games > 0 else 0.0,
        total_flatlines,
        round(100.0*total_flatlines/num_of_games, 2) if num_of_games > 0 else 0.0,
        total_runner_agenda_wins,
        round(100.0*total_runner_agenda_wins/num_of_games, 2) if num_of_games > 0 else 0.0,
        total_mills,
        round(100.0*total_mills/num_of_games, 2) if num_of_games > 0 else 0.0,
        total_draws,
        round(100.0*total_draws/num_of_games, 2) if num_of_games > 0 else 0.0
    ]

    player_stats = [
        (
            player,
            player_game_tally[player],
            player_win_tally[player],
            player_loss_tally[player],
            player_draw_tally[player],
            round(100.0*player_win_tally[player]/player_game_tally[player], 2) if player_game_tally[player] > 0 else 0.0,
            round(100.0*player_loss_tally[player]/player_game_tally[player], 2) if player_game_tally[player] > 0 else 0.0,
            round(100.0*player_draw_tally[player]/player_game_tally[player], 2) if player_game_tally[player] > 0 else 0.0,
        )
        for player in parts
    ]

    detail_player_stats = [
        (
            player,
            player_corp_game_tally[player],
            player_corp_agenda_win_tally[player],
            player_corp_flatline_tally[player],
            player_corp_agenda_loss_tally[player],
            player_corp_mill_tally[player],
            player_corp_draw_tally[player],
            player_runner_game_tally[player],
            player_runner_agenda_win_tally[player],
            player_runner_mill_tally[player],
            player_runner_agenda_loss_tally[player],
            player_runner_flatline_tally[player],
            player_runner_draw_tally[player],
        )
        for player in parts
    ]

    pair_matrix = [
        [player1]+[(pair_multiplicities[(player1, player2)] if not player1 == player2 else ' ') for player2 in parts]
        for player1 in parts
    ]
    pair_matrix = [[' ']+parts] + pair_matrix


    score_stats = [
        (
            player,
            player_score[player],
            player_sos[player],
        )
        for player in parts
    ]
    score_stats = sorted(score_stats, key=lambda t: (t[1], t[2]), reverse=True)


    context = {
        'season': season,
        'league': league,
        'games': games,
        'num_of_games': num_of_games,
        'foodbonuses': foodbonuses,
        'num_of_fbs': num_of_fbs,
        'dates': dates,
        'corp_stats': corp_stats,
        'runner_stats': runner_stats,
        'game_stats': game_stats,
        'player_stats': player_stats,
        'detail_player_stats': detail_player_stats,
        'pair_matrix': pair_matrix,
        'score_stats': score_stats,

    }
    return render(request, 'leaguemanager/season.html', context)