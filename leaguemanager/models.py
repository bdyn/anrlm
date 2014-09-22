from django.db import models
from django.contrib.auth.models import User
import datetime


class Player(models.Model):
    user = models.OneToOneField(User)
    favorite_faction = models.CharField(max_length=128)

    def __unicode__(self):
        return unicode(self.user)


class League(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Player, through='Membership')
    organizer = models.ForeignKey(Player, related_name='organizer', default=0)
        # there is a mistake here... one player should be able to run multiple leagues.  Fix this.
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
    # rules for the league

    def __unicode__(self):
        return self.name


class Game(models.Model):
    season = models.ForeignKey(Season, default=0)
    corp_player = models.ForeignKey(Player, related_name='corp_player')
    runner_player = models.ForeignKey(Player, related_name='runner_player')
    winner_choices = (
        ('draw', 'draw'),
        ('corp', 'corp'),
        ('runner', 'runner')
    )
    winner = models.CharField(max_length=8, choices=winner_choices, default='draw')
    date = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return '%s ran against %s in season: %s' % (self.runner_player, self.corp_player, self.season)

    @property
    def winning_player(self):
        if self.winner == "corp":
            return self.corp_player
        elif self.winner == "runner":
            return self.runner_player
        # Null for draws.
        return None

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
        return super(Game, self).save(*args, **kwargs)


class Scorecard(models.Model):
    player = models.ForeignKey(Player)
    season = models.ForeignKey(Season)

    def __unicode__(self):
        return '%s scorecard for %s' % (self.season, self.player)

    def games_played(self):
        # FIXME: Faster with Django Q objects
        # (https://docs.djangoproject.com/en/1.7/topics/db/queries/#complex-lookups-with-q-objects),
        # but simpler with two queries.
        games_played = list(self.season.game_set.filter(runner_player=self.player))
        games_played.extend(self.season.game_set.filter(corp_player=self.player))
        return games_played

    def games_won(self):
        return [g.winning_player == self.player for g in self.games_played()]
