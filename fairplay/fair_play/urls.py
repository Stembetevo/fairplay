from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import PlayerViewSet, TeamViewSet, AuthViewSet, MatchViewSet, HistoryViewSet

router = DefaultRouter()

router.register('players', PlayerViewSet, basename='player')
router.register('teams', TeamViewSet, basename='team')
router.register('auth', AuthViewSet, basename='auth')
router.register('matches', MatchViewSet, basename='match')
router.register('history', HistoryViewSet, basename='history')

urlpatterns = [
   path('api/', include(router.urls))
]