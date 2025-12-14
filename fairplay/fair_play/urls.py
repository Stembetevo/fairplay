from . import views
from django.urls import path

urlpatterns = [
    path('player/add/', views.CreatePlayerView.as_view(), name='playeradd'),
    path('players/', views.PlayerListView.as_view(), name='playerslist'),
]