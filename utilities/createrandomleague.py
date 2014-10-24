from django.contrib.auth.models import User
from leaguemanager.models import Player, League, Season, Game, Membership
import random
import datetime

playerlist = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Omega']
leaguename = 'Random League'
seasonname = 'Random Season'
number_of_games = 250
# FIXME: figure out how to implement food bonuses
# number_of_foodbonuses = 200

# create players (removed User, Player coupling)
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
	list_of_corp_IDs = [('Cerebral Imaging: Infinite Frontiers', 'HB Cerebral Imaging: Infinite Frontiers'),
		('Chronos Protocol (Hass-Bioroid): Selective Mind-mapping', 'Chronos Protocol (Hass-Bioroid): Selective Mind-mapping'),
		('Custom Biotics: Engineered for Success', 'Custom Biotics: Engineered for Success'),
		('Hass-Bioroid: Engineering the Future','Hass-Bioroid: Engineering the Future'),
		('Hass-Bioroid: Stronger Together', 'Hass-Bioroid: Stronger Together'),
		('NEXT Design: Guarding the Net', 'NEXT Design: Guarding the Net'),
		('The Foundary: Refining the Process', 'The Foundary: Refining the Process'),
		('Chronos Protocol (Jinteki): Selective Mind-mapping', 'Chronos Protocol (Jinteki): Selective Mind-mapping'),
		('Jinteki: Personal Evolution', 'Jinteki: Personal Evolution'),
		('Jinteki: Replicating Perfection', 'Jinteki: Replicating Perfection'),
		('Nisei Division: The Next Generation', 'Nisei Division: The Next Generation'),
		('Tennin Institute: The Secrets Within', 'Tennin Institute: The Secrets Within'),
		('NBN: Making News', 'NBN: Making News'),
		('NBN: The World is Yours', 'NBN: The World is Yours'),
		('Near-Earth Hub: Broadcast Center', 'Near-Earth Hub: Broadcast Center'),
		('Blue Sun: Powering the Future', 'Blue Sun: Powering the Future'),
		('Gagarin Deep Space: Expanding the Horizon', 'Gagarin Deep Space: Expanding the Horizon'),
		('GRNDL: Power Unleashed', 'GRNDL: Power Unleashed'),
		('Weyland Consortium: Because We Built It', 'Weyland Consortium: Because We Built It'),
		('Weyland Consortium: Buidling a Better World', 'Weyland Consortium: Buidling a Better World'),
		('The Shadow: Pulling the Strings', 'The Shadow: Pulling the Strings')]
	list_of_corp_IDs = map(lambda t: t[0], list_of_corp_IDs)
	corpID = random.choice(list_of_corp_IDs)
	list_of_runner_IDs =[('Edward Kim: Humanitys Hammer', 'Edward Kim: Humanitys Hammer'),
		('Noise: Hacker Extraordinaire', 'Noise: Hacker Extraordinaire'),
		('Quetzal: Free Spirit', 'Quetzal: Free Spirit'),
		('Reina Roja: Freedom Fighter', 'Reina Roja: Freedom Fighter'),
		('Whizzard: Master Gamer', 'Whizzard: Master Gamer'),
		('Andromeda: Dispossessed Ristie', 'Andromeda: Dispossessed Ristie'),
		('Gabriel Santiago: Consummate Professional', 'Gabriel Santiago: Consummate Professional'),
		('Iain Stirling: Retired Spook', 'Iain Stirling: Retired Spook'),
		('Ken Express Tenma: Disappeared Clone', 'Ken Express Tenma: Disappeared Clone'),
		('Laramy Fisk: Savvy Investor', 'Laramy Fisk: Savvy Investor'),
		('Leela Patel: Trained Pragmatist', 'Leela Patel: Trained Pragmatist'),
		('Silhouette: Stealth Operative', 'Silhouette: Stealth Operative'),
		('Chaos Theory: Wunderkind', 'Chaos Theory: Wunderkind'),
		('Exile: Streethawk', 'Exile: Streethawk'),
		('Kate Mac McCaffrey: Digital Tinker', 'Kate Mac McCaffrey: Digital Tinker'),
		('Nasir Meidan: Cyber Explorer', 'Nasir Meidan: Cyber Explorer'),
		('Rielle Kit Peddler: Transhuman', 'Rielle Kit Peddler: Transhuman'),
		('The Collective: Williams, Wu, et al.', 'The Collective: Williams, Wu, et al.'),
		('The Professor: Keeper of Knowledge', 'The Professor: Keeper of Knowledge'),
		('The Masque: Cyber General', 'The Masque: Cyber General')]
	list_of_runner_IDs = map(lambda t: t[0], list_of_runner_IDs)
	runnerID = random.choice(list_of_runner_IDs)    
	g = Game(season=s, corp_player=corpplayer, runner_player=runnerplayer, outcome=outcome, date=gamedate, corp_ID=corpID, runner_ID=runnerID)
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


	