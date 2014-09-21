from django.contrib import admin
from leaguemanager.models import Player, League, Membership, Game, Season, Scorecard


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0


class SeasonInline(admin.StackedInline):
    model = Season
    extra = 0


class LeagueAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, SeasonInline]


class GameInline(admin.TabularInline):
    model = Game
    extra = 0


class ScorecardInline(admin.StackedInline):
    model = Scorecard
    extra = 0


class SeasonAdmin(admin.ModelAdmin):
    inlines = [GameInline, ScorecardInline]


class PlayerAdmin(admin.ModelAdmin):
    inlines = [ScorecardInline]


admin.site.register(Player, PlayerAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Game)
admin.site.register(Scorecard)
admin.site.register(Membership)
