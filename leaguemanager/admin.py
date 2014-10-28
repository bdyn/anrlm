from django.contrib import admin
from leaguemanager.models import Player, League, Membership, Game, Season, FoodBonus


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



class SeasonAdmin(admin.ModelAdmin):
    inlines = [GameInline]




admin.site.register(Player)
admin.site.register(League, LeagueAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Game)
admin.site.register(Membership)
admin.site.register(FoodBonus)
