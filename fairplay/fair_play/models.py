from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class Player(models.Model):
    class Position(models.TextChoices):
        ST = 'Striker'
        DF = 'Defender'
        MD = 'MidFielder'
        GK = 'GoalKeeper'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='players')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_players')
    position = models.CharField(
        max_length = 10,
        choices=Position.choices 
    )
    rating = models.IntegerField(
        default=70,
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        help_text="Player skill rating (50-100)"
    )
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null= True, blank=True, related_name='players')

    @property
    def name(self):
        return self.user.username
    
    def __str__(self):
        return f"{self.user.username}"
    class Meta:
        ordering = ['user__username']
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_position = models.CharField(
        max_length=20,
        choices = Player.Position.choices,
        default=Player.Position.ST
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
     
@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Team(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')
    members = models.ManyToManyField(User, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Match(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'Scheduled', 'Scheduled'
        PLAYED = 'Played', 'Played'
        CANCELLED = 'Cancelled', 'Cancelled'
    
    date_created = models.DateTimeField(auto_now_add=True)
    played_at = models.DateTimeField(null=True, blank=True, help_text="When the match is/was scheduled")
    location = models.CharField(max_length=200, blank=True, help_text="Match venue")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )
    team_A = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teamA')
    team_B = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teamB')
    score_a = models.IntegerField(null=True, blank=True, help_text="Team A goals")
    score_b = models.IntegerField(null=True, blank=True, help_text="Team B goals")

    def __str__(self):
        if self.score_a is not None and self.score_b is not None:
            return f"{self.team_A} {self.score_a} - {self.score_b} {self.team_B}"
        return f"{self.team_A} vs {self.team_B}"
    
    @property
    def winner(self):
        """Returns winning team or None for draw/unplayed"""
        if self.score_a is None or self.score_b is None:
            return None
        if self.score_a > self.score_b:
            return self.team_A
        elif self.score_b > self.score_a:
            return self.team_B
        return None  # Draw
    
    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Matches'


class TeamMembership(models.Model):
    """Track historical team memberships for players"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='memberships')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True, help_text="When player left the team")
    
    def __str__(self):
        status = "current" if self.left_at is None else f"left {self.left_at.strftime('%Y-%m-%d')}"
        return f"{self.player.user.username} in {self.team.name} ({status})"
    
    class Meta:
        ordering = ['-joined_at']
        verbose_name_plural = 'Team Memberships'


class MatchParticipation(models.Model):
    """Track which players participated in which matches"""
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='participations')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_participations')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='match_participations')
    minutes_played = models.IntegerField(null=True, blank=True, help_text="Minutes played in the match")
    goals = models.IntegerField(default=0, help_text="Goals scored")
    assists = models.IntegerField(default=0, help_text="Assists made")
    match_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Match performance rating (1-10)"
    )
    
    def __str__(self):
        return f"{self.player.user.username} in {self.match}"
    
    class Meta:
        ordering = ['-match__date_created']
        unique_together = ['match', 'player']  # Player can only participate once per match
