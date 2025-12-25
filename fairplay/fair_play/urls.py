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
    path('teams/<int:team_id>/history/', views.team_history_view, name='team_history'),
    
    # Match URLs
    path('matches/', views.match_list_view, name='match_list'),
    path('matches/create/', views.match_create_view, name='match_create'),
    path('matches/<int:pk>/', views.match_detail_view, name='match_detail'),
    path('matches/<int:pk>/result/', views.match_record_result_view, name='match_record_result'),
    
    # History URLs
    path('history/', views.my_history_view, name='my_history'),
]