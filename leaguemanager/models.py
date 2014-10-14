from django.db import models
#from django.contrib.auth.models import User
import datetime


class Player(models.Model):
    # remove user from the player model
    # not going to deal with user logins right now
    # user = models.OneToOneField(User)
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
        # but simpler with two queries.
        games_played = list(season.game_set.filter(runner_player=self))
        games_played.extend(season.game_set.filter(corp_player=self))
        return games_played

    def games_won(self, season):
        return [g for g in self.games_played(season) if g.winning_player == self]

    def games_won_on_date(self, season, date):
        return [g for g in self.games_won(season) if g.date == date]

    def dates_attended(self, season):
        # output = [g.date for g in self.games_played(season)]
        # output.delete_duplicates()
        # return output
        output = []
        game_dates = [g.date for g in self.games_played(season)]
        for date in game_dates:
            if not date in output:
                output.append(date)
        return output

    def score(self, season):
        total = 0
        total += len(self.games_played(season))
        total += 5*len(self.dates_attended(season))
        for date in self.dates_attended(season):
            total += min(5, len(self.games_won_on_date(season, date)))
        return total
       


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


class Game(models.Model):
    season = models.ForeignKey(Season, default=0)
    corp_player = models.ForeignKey(Player, related_name='corp_player')
    runner_player = models.ForeignKey(Player, related_name='runner_player')
    outcome_choices = (
        ('draw', 'draw'),
        ('corp agenda victory', 'corp agenda victory'),
        ('runner agenda victory', 'runner agenda victory'),
        ('flatline', 'flatline'),
        ('mill', 'mill')
    )
    outcome = models.CharField(max_length=22, choices=outcome_choices, default='draw')
    date = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return '%s ran against %s in season: %s' % (self.runner_player, self.corp_player, self.season)

    @property
    def winning_player(self):
        if self.outcome == 'corp agenda victory' or self.outcome == 'flatline':
            return self.corp_player
        elif self.outcome == 'runner agenda victory' or self.outcome == 'mill':
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




# removing the scorecard class
# these methods should be functions of a player and a season
# for now, I will move these methods to the player class
'''
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
        return [g for g in self.games_played() if g.winning_player == self.player]

    def food_bonus_dates(self):
        return [foodbonus.date for foodbonus in self.foodbonus_set.all()]

    def point_total(self):
        total = 0
        for g in self.games_played():
            additional_points = 1
            if g in self.games_won():
                additional_points = additional_points + 2
            if g.date in self.food_bonus_dates():
                additional_points = 2*additional_points
            total = total + additional_points
        return total
'''

# this food bonus will be merged with a new rules/points paradigm
'''
class FoodBonus(models.Model):
    # At Raygun, we get 2x points if we buy food.
    scorecard = models.ForeignKey(Scorecard)
    date = models.DateField(default=datetime.date.today())

    def __unicode__(self):
        return 'On %s for %s' % (self.date, self.scorecard.player)
'''

