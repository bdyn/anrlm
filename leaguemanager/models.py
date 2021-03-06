from django.db import models
#from django.contrib.auth.models import User
import datetime

from ID_lists import *


class Player(models.Model):
    name = models.CharField(max_length=128, default='handle')
    first_name = models.CharField(max_length=128, default='first')
    last_name = models.CharField(max_length=128, default='last')
    email_address = models.CharField(max_length=128, default='email')
    faction_choices = (
        ('neutral', 'neutral'),
        ('anarch', 'anarch'),
        ('criminal', 'criminal'),
        ('shaper', 'shaper'),
        ('haas-bioroid', 'haas-bioroid'),
        ('jinteki', 'jinteki'),
        ('nbn', 'nbn'),
        ('weyland', 'weyland'),
    )
    favorite_faction = models.CharField(max_length=13, choices=faction_choices, default='neutral')

    def __unicode__(self):
        return unicode(self.name)  

    def games_played(self, season):
        # FIXME: Faster with Django Q objects
        # (https://docs.djangoproject.com/en/1.7/topics/db/queries/#complex-lookups-with-q-objects),
        # but simpler with two queries.Season
        games_played = list(season.game_set.filter(runner_player=self))
        games_played.extend(season.game_set.filter(corp_player=self))
        # not sure which is best
        #games_played = list(Game.objects.filter(runner_player=self, season=season))
        #games_played.extend(Game.objects.filter(corp_player=self, season=season))
        return games_played

    def games_won(self, season):
        return [g for g in self.games_played(season) if g.winning_player == self]

    def games_won_on_date(self, season, date):
        return [g for g in self.games_won(season) if g.date == date]

    def dates_attended(self, season):
        return {g.date for g in self.games_played(season)}        

    def score(self, season):
        total = 0
        total += len(self.games_played(season))
        total += 5*len(self.dates_attended(season))
        for date in self.dates_attended(season):
            total += min(5, len(self.games_won_on_date(season, date)))
        total += 5*len(self.foodbonus_set.filter(season=season))
        return total

    def food_on_date(self, season, date):
        return FoodBonus.objects.filter(player=self, season=season, date=date).count()

    def games_played_on_date(self, season, date):
        return len([x for x in self.games_played(season=season) if x.date==date])






class League(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Player, through='Membership')
    organizer = models.ForeignKey(Player, related_name='organizer', default=0)
    
    def __unicode__(self):
        return self.name





class Membership(models.Model):
    player = models.ForeignKey(Player)
    league = models.ForeignKey(League)
    date_joined = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return '%s is in %s' % (self.player, self.league)





class Season(models.Model):
    name = models.CharField(max_length=128)
    league = models.ForeignKey(League)
    begin_date = models.DateField(default=datetime.date.today())
    end_date = models.DateField(default=datetime.date.today()+datetime.timedelta(days=30))

    def __unicode__(self):
        return self.name

    @property    
    def participants(self):
        parts = set([])
        for game in self.game_set.all():
            parts.update(game.players)
        for fb in FoodBonus.objects.filter(season=self):
            parts.update([fb.player])
        return list(parts)






class Game(models.Model):
    # meta options for the model to index
    # index on runner and corp (possibly with season)
    # start with a keyword option
    season = models.ForeignKey(Season, default=0, db_index=True)
    corp_player = models.ForeignKey(Player, related_name='corp_player', db_index=True)
    corp_ID_choices = tuple(zip(corp_ID_list(), corp_ID_list()))
    corp_ID = models.CharField(max_length=128, choices=corp_ID_choices, default='none')
    runner_player = models.ForeignKey(Player, related_name='runner_player', db_index=True)
    runner_ID_choices = tuple(zip(runner_ID_list(), runner_ID_list()))
    runner_ID = models.CharField(max_length=128, choices=runner_ID_choices, default='none')
    outcome_choices = (
        ('draw', 'draw'),
        ('corp agenda victory', 'corp agenda victory'),
        ('runner agenda victory', 'runner agenda victory'),
        ('flatline', 'flatline'),
        ('mill', 'mill')
    )
    outcome = models.CharField(max_length=22, choices=outcome_choices, default='draw')
    date = models.DateField(default=datetime.date.today(), db_index=True)

    def __unicode__(self):
        return '%s ran against %s in season: %s' % (self.runner_player, self.corp_player, self.season)
    
    
    class Meta:
        index_together = [
            ['corp_player', 'season'],
            ['runner_player', 'season'],
            ['season', 'runner_player'],
            ['season', 'corp_player'],
        ]
    

    @property
    def winning_player(self):
        if self.outcome == 'corp agenda victory' or self.outcome == 'flatline':
            return self.corp_player
        elif self.outcome == 'runner agenda victory' or self.outcome == 'mill':
            return self.runner_player
        return None

    @property
    def players(self):
        return [self.corp_player, self.runner_player]

    def _is_legal(self):
        # If possible, fail before making expensive database queries.
        if self.corp_player == self.runner_player:
            return False

        season = self.season
        if not (season.begin_date <= self.date <= season.end_date):
            return False

        players = set(season.league.members.all())
        if self.runner_player not in players or self.corp_player not in players:
            return False

        return True

    def save(self, *args, **kwargs):
        if not self._is_legal():
            raise ValueError("Can't save illegal game %s." % self)
        # this is where you would invalidate the cache.
        return super(Game, self).save(*args, **kwargs)





class FoodBonus(models.Model):
    player = models.ForeignKey(Player)
    season = models.ForeignKey(Season)
    date = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return 'On %s for %s in %s' % (self.date, self.player, self.season)

    class Meta:
        ordering = ['date', 'player']