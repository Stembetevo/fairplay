# FairPlay: SPA + REST Backend Migration Guide

This guide explains how to integrate the new Vite React frontend with your existing Django backend to build a full SPA + REST API architecture.

## What Changed

Your FairPlay app has been enhanced with a modern frontend:

```
OLD: User Request → Django View (renders HTML template) → HTML Response

NEW: User Request → React App (SPA) → API Call → Django REST API → JSON RES
ponse
```

## Step 1: Convert Django Views to REST API Endpoints

Your current Django views return HTML via templates. They need to be converted to return JSON so the React frontend can consume them.

### Install Django REST Framework

```bash
cd fairplay
pip install djangorestframework django-cors-headers
```

### Update `fairplay/settings.py`

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... existing apps
    'rest_framework',
    'corsheaders',
    'fair_play',
]
```

Add CORS and REST Framework config:
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this before SessionMiddleware
    # ... rest of middleware
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
    # Add your production domains here
]

CORS_ALLOW_CREDENTIALS = True
```

## Step 2: Create API Serializers

Create `fairplay/fair_play/serializers.py`:

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Player, Team, Match, TeamMembership, MatchParticipation, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['preferred_position', 'bio']

class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Player
        fields = ['id', 'username', 'owner_id', 'position', 'rating', 'team_id', 'team_name']

class TeamSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    players = PlayerSerializer(many=True, read_only=True)
    members_count = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'owner_id', 'owner_username', 'members_count', 'total_rating', 'avg_rating', 'players']
    
    def get_members_count(self, obj):
        return obj.members.count()
    
    def get_total_rating(self, obj):
        return sum(p.rating for p in obj.players.all())
    
    def get_avg_rating(self, obj):
        players = obj.players.all()
        return sum(p.rating for p in players) / players.count() if players else 0

# Add more serializers for Match, TeamMembership, MatchParticipation as needed
```

## Step 3: Create API Views and Endpoints

Create `fairplay/fair_play/api_views.py` with REST API views:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Player, Team, Match
from .serializers import PlayerSerializer, TeamSerializer, UserSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Player.objects.filter(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        
        player = Player.objects.create(
            user=user,
            owner=request.user,
            position=request.data.get('position_override', user.profile.preferred_position),
            rating=request.data.get('rating', 70)
        )
        
        return Response(PlayerSerializer(player).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def reset(self, request):
        Player.objects.filter(owner=request.user).delete()
        return Response({'status': 'Players reset'})

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Team.objects.filter(owner=request.user)
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        # Your existing generate_balanced_teams logic here
        pass

# Add auth endpoints
class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(None)
        return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid credentials'}, status=400)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'status': 'logged out'})
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        # User registration logic
        pass
    
    @action(detail=False, methods=['get'])
    def csrf(self, request):
        # Return CSRF token in a cookie (Django handles this automatically)
        return Response({'status': 'Set-Cookie'})
```

## Step 4: Update URLs

Update `fairplay/fair_play/urls.py`:

```python
from rest_framework.routers import DefaultRouter
from .api_views import PlayerViewSet, TeamViewSet, AuthViewSet

router = DefaultRouter()
router.register('players', PlayerViewSet, basename='player')
router.register('teams', TeamViewSet, basename='team')
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## Step 5: Run Both Servers

### Terminal 1: Django Backend

```bash
cd fairplay/fairplay
python manage.py runserver 8000
```

### Terminal 2: Vite Frontend

```bash
cd fairplay/frontend
npm run dev
```

Visit `http://localhost:5173` to see the app.

## Step 6: Test the Integration

1. Register a new account
2. Add players by searching for other registered users
3. Generate teams
4. Create and manage matches
5. View your history

## Complete API Endpoints Reference

See `frontend/README.md` for the full API contract that the frontend expects.

## Next Steps

1. Implement all serializers and API views
2. Add proper error handling and validation
3. Write tests for API endpoints
4. Deploy both backend and frontend to your hosting provider
5. Gradually migrate from template-based views to API-only views
6. Keep old template routes for backwards compatibility during transition

## Production Deployment

Once complete, you can:
- Deploy Django to a server (Heroku, AWS, Azure, DigitalOcean)
- Build the frontend: `npm run build` → deploy `dist/` to static hosting (Vercel, GitHub Pages, Netlify)
- Or serve both from the same Django instance by pointing static files to the built frontend

## Questions?

Refer to:
- Django REST Framework docs: https://www.django-rest-framework.org/
- React docs: https://react.dev/
- Vite docs: https://vite.dev/
