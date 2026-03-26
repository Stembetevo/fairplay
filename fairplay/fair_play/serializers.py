from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Player, Team, TeamMembership, Match, MatchParticipation, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['preferred_position', 'bio']


class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    owner_id = serializers.IntegerField(read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True, allow_null=True)

    class Meta:
        model = Player
        fields = ['id', 'username', 'owner_id', 'position', 'rating', 'team_id', 'team_name']


class TeamSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_id = serializers.IntegerField(read_only=True)
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


class TeamMembershipSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.user.username', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = TeamMembership
        fields = ['id', 'player_name', 'team_name', 'joined_at', 'left_at']


class MatchParticipationSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.user.username', read_only=True)
    player_position = serializers.CharField(source='player.position', read_only=True)
    player_rating = serializers.IntegerField(source='player.rating', read_only=True)

    class Meta:
        model = MatchParticipation
        fields = ['id', 'player_name', 'player_position', 'player_rating', 'goals', 'assists', 'match_rating', 'minutes_played']


class MatchSerializer(serializers.ModelSerializer):
    team_A_name = serializers.CharField(source='team_A.name', read_only=True)
    team_B_name = serializers.CharField(source='team_B.name', read_only=True)
    participations = MatchParticipationSerializer(many=True, read_only=True)
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'team_A', 'team_A_name', 'team_B', 'team_B_name', 'played_at', 'location', 
                  'status', 'score_a', 'score_b', 'date_created', 'participations', 'can_edit']
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        # Allow editing if user is owner of either team
        return obj.team_A.owner == request.user or obj.team_B.owner == request.user


class MyHistoryResponseSerializer(serializers.Serializer):
    """Aggregated user statistics"""
    total_matches = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    total_goals = serializers.IntegerField()
    total_assists = serializers.IntegerField()
    memberships = TeamMembershipSerializer(many=True)
    participations = MatchParticipationSerializer(many=True)

