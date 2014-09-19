from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Player(models.Model):
	user = models.OneToOneField(User)
	favorite_faction = models.CharField(max_length=128)
	
	def xyz(self):
		return True
	# add addition data to user object

	def __str__(self):
		return self.user.username

	
class League(models.Model):
	name = models.CharField(max_length=128)
	members = models.ManyToManyField(Player, through='Membership')
	organizer = models.OneToOneField(Player, related_name='organizer', default=0)

	def __str__(self):
		return self.name


class Membership(models.Model):
	player = models.ForeignKey(Player)
	league = models.ForeignKey(League)
	date_joined = models.DateField(default=datetime.date.today())

	def __str__(self):
		return '%s is in %s' % (self.player, self.league)




class Season(models.Model):
	name = models.CharField(max_length=128)
	league = models.ForeignKey(League)
	begin_date = models.DateField(default=datetime.date.today())
	end_date = models.DateField(default=datetime.date.today())
	# rules for the league

	def __str__(self):
		return self.name 


class Game(models.Model):
	season = models.ForeignKey(Season, default=0)
	corp_player = models.ForeignKey(Player, related_name='corp_player')
	runner_player = models.ForeignKey(Player, related_name='runner_player')
	winner_choices = (
		('draw','draw'), 
		('corp','corp'), 
		('runner','runner')
	)
	winner = models.CharField(max_length=8, choices=winner_choices, default='draw')
	date = models.DateField(default=datetime.date.today())

	def is_legal(self):
		return (self.corp_player != self.runner_player) and (self.runner_player in self.season.league.members.all()) and ((self.corp_player in self.season.league.members.all()))
	
	def __str__(self):
		return '%s ran against %s in season: %s' % (self.runner_player, self.corp_player, self.season) 


class Scorecard(models.Model):
	player = models.ForeignKey(Player)
	season = models.ForeignKey(Season)
	
	def __str__(self):
		return '%s scorecard for %s' % (self.season, self.player)

