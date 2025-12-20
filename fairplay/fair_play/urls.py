from . import views
from django.urls import path

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Player URLs
    path('player/add/', views.add_player_view, name='playeradd'),
    path('players/', views.PlayerListView.as_view(), name='playerslist'),
    path('player/<int:pk>/delete/', views.DeletePlayerView.as_view(), name='playerdelete'),
    path('player/<int:pk>/update/', views.UpdatePlayerView.as_view(), name='playerupdate'),
    path('reset/', views.reset_players, name='reset'),
    
    # Team URLs
    path('teams/generate/', views.team_form_view, name='team_form'),
    path('teams/create/', views.generate_teams_view, name='generate_teams'),
    path('teams/', views.teams_display_view, name='teams_display'),
]