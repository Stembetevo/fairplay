from . import views
from django.urls import path

urlpatterns = [
    path('register',),
    path('player/add/', views.CreatePlayerView.as_view(), name='playeradd'),
    path('players/', views.PlayerListView.as_view(), name='playerslist'),
    path('player/<int:pk>/delete/', views.DeletePlayerView.as_view(), name='playerdelete'),
    path('player/<int:pk>/update/', views.UpdatePlayerView.as_view(), name='playerupdate'),
    path('reset/', views.reset_players, name='reset'),
    path('teams/generate/', views.team_form_view, name='team_form'),
    path('teams/create/', views.generate_teams_view, name='generate_teams'),
    path('teams/', views.teams_display_view, name='teams_display'),
]