from . import views
from django.urls import path

urlpatterns = [
    path('player/add/', views.CreatePlayerView.as_view(), name='playeradd'),
    path('players/', views.PlayerListView.as_view(), name='playerslist'),
    path('player/<int:pk>/delete/', views.DeletePlayerView.as_view(), name='playerdelete'),
    path('player/<int:pk>/update/', views.UpdatePlayerView.as_view(), name='playerupdate'),
    path('reset/', views.reset_players, name='reset'),
]