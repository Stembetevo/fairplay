from django.db import models

# Create your models here.
class Player(models.Model):
    class Position(models.TextChoices):
        ST = 'Striker'
        DF = 'Defender'
        MD = 'MidFielder'
        GK = 'GoalKeeper'

    name = models.CharField(max_length=200)
    position = models.CharField(
        max_length = 10,
        choices=Position.choices 
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Team(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(Player, related_name='teams' ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    
