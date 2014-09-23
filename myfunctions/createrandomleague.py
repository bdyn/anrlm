from django.contrib.auth.models import User
from leaguemanager.models import Player, League, Membership, Season, Game, Scorecard
import random
import datetime



playerlist = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Omega']
leaguename = 'RLeague'
seasonname = 'RSeason'
number_of_games = 50



# create users
for name in playerlist:
	try:
		u = User.objects.get(username=name)
	except u.DoesNotExist:
		u = User.objects.create_user(name, name + '@anrlm.com', name)

# register users as players
for name in playerlist:
	u = User.objects.get(username=name)
	try:
		p = Player.objects.get(user=u)
	except p.DoesNotExist:
		p = Player(user=u)
		p.save()

# create league for players
try:
	l = League.objects.get(name=leaguename)
except l.DoesNotExist:
	organizingplayer = User.objects.get(username=playerlist[0]).player
	l = League(name=leaguename, organizer=organizingplayer)
	l.save()

# enroll players in league
l = League.objects.get(name=leaguename)
for name in playerlist:
	p = User.objects.get(username=name).player
	try:
		m = Membership.objects.get(player=p, league=l)
	except m.DoesNotExist:
		m = Membership(player=p, league=l)
		m.save()

# create a season for the players
l = League.objects.get(name=leaguename)
try: 
	s = Season.objects.get(name=seasonname, league=l)
except s.DoesNotExist:
	s = Season(name=seasonname, league=l)
	s.save()

# create a scorecard for each player
l = League.objects.get(name=leaguename)
s = Season.objects.get(name=seasonname, league=l)
for name in playerlist:
	p = User.objects.get(username=name).player
	try:
		sc = Scorecard.objects.get(player=p, season=s)
	except sc.DoesNotExist:
		sc = Scorecard(player=p, season=s)
		sc.save()

# now we will generate random games
l = League.objects.get(name=leaguename)
s = Season.objects.get(name=seasonname, league=l)
while len(s.game_set.all()) < number_of_games:
	corpplayer = random.choice(playerlist)
	runnerplayer = corpplayer
	while runnerplayer == corpplayer:
		runnerplayer = random.choice(playerlist)
	corpplayer = User.objects.get(username=corpplayer).player
	runnerplayer = User.objects.get(username=runnerplayer).player
	gamewinner = random.choice(['draw', 'runner', 'corp'])
	random_number_of_days = random.choice(range(30))
	gamedate = s.begin_date + datetime.timedelta(days=random_number_of_days)
	g = Game(season=s, corp_player=corpplayer, runner_player=runnerplayer, winner=gamewinner, date=gamedate)
	g.save()

	