from django.contrib.auth.models import User
from leaguemanager.models import Player, League, Season, Game, Membership
import random
import datetime

playerlist = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Omega']
leaguename = 'Random League'
seasonname = 'Random Season'
number_of_games = 1000
# FIXME: figure out how to implement food bonuses
# number_of_foodbonuses = 200

# register users as players (removed User, Player coupling)
for name in playerlist:
	try:
		p = Player.objects.get(name=name)
	except Player.DoesNotExist:
		p = Player(name=name)
		p.save()

# create league for players
try:
	l = League.objects.get(name=leaguename)
except League.DoesNotExist:
	organizingplayer = Player.objects.get(name=playerlist[0])
	l = League(name=leaguename, organizer=organizingplayer)
	l.save()

# enroll players in league
l = League.objects.get(name=leaguename)
for name in playerlist:
	p = Player.objects.get(name=name)
	try:
		m = Membership.objects.get(player=p, league=l)
	except Membership.DoesNotExist:
		m = Membership(player=p, league=l)
		m.save()

# create a season for the players
l = League.objects.get(name=leaguename)
try: 
	s = Season.objects.get(name=seasonname, league=l)
except Season.DoesNotExist:
	s = Season(name=seasonname, league=l)
	s.save()

# now we will generate random games
l = League.objects.get(name=leaguename)
s = Season.objects.get(name=seasonname, league=l)
while len(s.game_set.all()) < number_of_games:
	corpplayer = random.choice(playerlist)
	runnerplayer = corpplayer
	while runnerplayer == corpplayer:
		runnerplayer = random.choice(playerlist)
	corpplayer = Player.objects.get(name=corpplayer)
	runnerplayer = Player.objects.get(name=runnerplayer)
	outcome = random.choice(['draw', 'corp agenda victory', 'runner agenda victory', 'flatline', 'mill'])
	random_number_of_days = random.choice(range(30))
	gamedate = s.begin_date + datetime.timedelta(days=random_number_of_days)
	g = Game(season=s, corp_player=corpplayer, runner_player=runnerplayer, outcome=outcome, date=gamedate)
	g.save()

# removed Scorecard 

# needs to be updated
'''
# and random food bonuses
l = League.objects.get(name=leaguename)
s = Season.objects.get(name=seasonname, league=l)
def all_food_bonus_objects():
	temp = []
	for sc in s.scorecard_set.all():
		temp.extend(sc.food_bonus_dates())
	return temp
while len(all_food_bonus_objects()) < number_of_foodbonuses:
	p = random.choice(playerlist)
	p = User.objects.get(username=p).player
	random_number_of_days = random.choice(range(30))
	fooddate = s.begin_date + datetime.timedelta(days=random_number_of_days)
	scorecard = Scorecard.objects.get(player=p, season=s)
	f = FoodBonus(date=fooddate, scorecard=scorecard)
	f.save()

'''


	