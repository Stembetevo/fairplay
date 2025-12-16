from django.contrib import admin
from .models import Player, Team, Match

# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'rating', 'team')
    list_filter = ('position', 'rating', 'team')
    search_fields = ('name',)
    ordering = ('-rating', 'name')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'player_count', 'total_rating')
    search_fields = ('name',)
    ordering = ('-created_at',)
    
    def player_count(self, obj):
        return obj.players.count()
    player_count.short_description = 'Players'
    
    def total_rating(self, obj):
        return sum(player.rating for player in obj.players.all())
    total_rating.short_description = 'Total Rating'

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team_A', 'team_B', 'date_created')
    list_filter = ('date_created',)
    ordering = ('-date_created',)
