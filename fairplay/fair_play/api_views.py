from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Player, Team, Match, TeamMembership, MatchParticipation, User
from .serializers import (
    PlayerSerializer, TeamSerializer, UserSerializer, MatchSerializer,
    TeamMembershipSerializer, MatchParticipationSerializer, MyHistoryResponseSerializer
)
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q, Sum, Count, F
from datetime import datetime
import random


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(None)
        return Response(UserSerializer(request.user).data)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid credentials'}, status=400)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response({'status': 'Logged out'})
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        position = request.data.get('position', 'Striker')
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.preferred_position = position
        user.profile.save()
        
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def csrf(self, request):
        return Response({'status': 'CSRF cookie set'})


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Player.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': f'User {username} not found'}, status=400)

        position = request.data.get('position_override', user.profile.preferred_position)
        rating = request.data.get('rating', 70)
        
        player = Player.objects.create(
            user=user,
            owner=request.user,
            position=position,
            rating=rating
        )

        return Response(PlayerSerializer(player).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def reset(self, request):
        Player.objects.filter(owner=request.user).delete()
        return Response({'status': 'All players reset'})


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        owned = Team.objects.filter(owner=user)
        member = Team.objects.filter(members=user)
        return (owned | member).distinct()
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate balanced teams using snake draft algorithm"""
        num_teams = request.data.get('num_teams', 2)
        team_names = request.data.get('team_names', [f'Team {i+1}' for i in range(num_teams)])
        
        # Get all available players (owned by user)
        players = list(Player.objects.filter(owner=request.user).order_by('-rating'))
        
        if not players:
            return Response({'error': 'No players available'}, status=400)
        
        # Snake draft: alternate picking highest rated players
        teams_data = [[] for _ in range(num_teams)]
        forward = True
        
        while players:
            if forward:
                for i in range(num_teams):
                    if players:
                        player = players.pop(0)
                        teams_data[i].append(player)
            else:
                for i in range(num_teams - 1, -1, -1):
                    if players:
                        player = players.pop(0)
                        teams_data[i].append(player)
            forward = not forward
        
        # Create teams
        created_teams = []
        for i, players_list in enumerate(teams_data):
            team_name = team_names[i] if i < len(team_names) else f'Team {i+1}'
            team = Team.objects.create(name=team_name, owner=request.user)
            
            # Add players to team
            for player in players_list:
                player.team = team
                player.save()
                # Create membership record
                TeamMembership.objects.create(player=player, team=team)
            
            # Add team members
            team.members.add(request.user)
            team.save()
            
            created_teams.append(team)
        
        return Response(
            {'owned_teams': TeamSerializer(created_teams, many=True).data, 'member_teams': []},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get team history including stats and memberships"""
        team = self.get_object()
        
        # Check permission
        if team.owner != request.user and request.user not in team.members.all():
            return Response({'error': 'Permission denied'}, status=403)
        
        # Get all matches for this team
        team_matches = Match.objects.filter(Q(team_A=team) | Q(team_B=team))
        
        # Calculate stats
        wins = 0
        draws = 0
        losses = 0
        goals_for = 0
        goals_against = 0
        
        for match in team_matches:
            if match.status == 'Played' and match.score_a is not None and match.score_b is not None:
                if match.team_A == team:
                    goals_for += match.score_a
                    goals_against += match.score_b
                    if match.score_a > match.score_b:
                        wins += 1
                    elif match.score_a == match.score_b:
                        draws += 1
                    else:
                        losses += 1
                else:  # team is team_B
                    goals_for += match.score_b
                    goals_against += match.score_a
                    if match.score_b > match.score_a:
                        wins += 1
                    elif match.score_a == match.score_b:
                        draws += 1
                    else:
                        losses += 1
        
        memberships = TeamMembership.objects.filter(team=team)
        
        return Response({
            'team': TeamSerializer(team).data,
            'stats': {
                'wins': wins,
                'draws': draws,
                'losses': losses,
                'goals_for': goals_for,
                'goals_against': goals_against
            },
            'memberships': TeamMembershipSerializer(memberships, many=True).data
        })


class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Match.objects.filter(Q(team_A__owner=user) | Q(team_A__members=user) | 
                                    Q(team_B__owner=user) | Q(team_B__members=user)).distinct()
    
    def create(self, request, *args, **kwargs):
        team_a_id = request.data.get('team_A')
        team_b_id = request.data.get('team_B')
        
        try:
            team_a = Team.objects.get(id=team_a_id)
            team_b = Team.objects.get(id=team_b_id)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=400)
        
        if team_a == team_b:
            return Response({'error': 'Cannot create match between same team'}, status=400)
        
        match = Match.objects.create(
            team_A=team_a,
            team_B=team_b,
            played_at=request.data.get('played_at'),
            location=request.data.get('location', '')
        )
        
        return Response(MatchSerializer(match, context={'request': request}).data, 
                       status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch', 'post'])
    def result(self, request, pk=None):
        """Record or update match result"""
        match = self.get_object()
        
        # Check permission
        if match.team_A.owner != request.user and match.team_B.owner != request.user:
            return Response({'error': 'Permission denied'}, status=403)
        
        score_a = request.data.get('score_a')
        score_b = request.data.get('score_b')
        
        if score_a is None or score_b is None:
            return Response({'error': 'Missing scores'}, status=400)
        
        match.score_a = score_a
        match.score_b = score_b
        match.status = 'Played'
        match.played_at = request.data.get('played_at') or match.played_at or datetime.now()
        match.save()
        
        return Response(MatchSerializer(match, context={'request': request}).data)


class HistoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get user's personal match history and aggregate stats"""
        user = request.user
        
        # Get user's team memberships
        memberships = TeamMembership.objects.filter(player__owner=user)
        
        # Get user's match participations
        participations = MatchParticipation.objects.filter(player__owner=user)
        
        # Calculate stats
        user_matches = Match.objects.filter(
            Q(team_A__owner=user) | Q(team_A__members=user) |
            Q(team_B__owner=user) | Q(team_B__members=user)
        ).filter(status='Played').distinct()
        
        wins = 0
        draws = 0
        losses = 0
        
        for match in user_matches:
            if match.score_a is not None and match.score_b is not None:
                # Check if user was on team_A
                if user in match.team_A.members.all() or match.team_A.owner == user:
                    if match.score_a > match.score_b:
                        wins += 1
                    elif match.score_a == match.score_b:
                        draws += 1
                    else:
                        losses += 1
                # Check if user was on team_B
                elif user in match.team_B.members.all() or match.team_B.owner == user:
                    if match.score_b > match.score_a:
                        wins += 1
                    elif match.score_a == match.score_b:
                        draws += 1
                    else:
                        losses += 1
        
        total_goals = participations.aggregate(Sum('goals'))['goals__sum'] or 0
        total_assists = participations.aggregate(Sum('assists'))['assists__sum'] or 0
        
        data = {
            'total_matches': user_matches.count(),
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'total_goals': total_goals,
            'total_assists': total_assists,
            'memberships': TeamMembershipSerializer(memberships, many=True).data,
            'participations': MatchParticipationSerializer(participations, many=True).data
        }
        
        return Response(data)