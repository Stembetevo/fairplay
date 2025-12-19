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
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Match(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    team_A = models.ForeignKey(Team,on_delete=models.CASCADE, related_name='teamA')
    team_B = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teamB')

    def __str__(self):
        return f"{self.team_A} vs {self.team_B}"
    
    class Meta:
        ordering = ['-date_created']
    
