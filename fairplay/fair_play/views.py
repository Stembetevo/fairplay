from django.shortcuts import render
from .forms import PlayerCreationForm
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Player, Team
from django.shortcuts import redirect

# Create your views here.
def index(request):
    #Main page view
    return render(request, 'index.html')


class CreatePlayerView(CreateView):
    form_class = PlayerCreationForm
    template_name = 'playeradd.html'
    success_url = reverse_lazy('playerslist')

    def form_valid(self, form):
        messages.success(self.request, 'Player added successfully')
        return super().form_valid(form)


class PlayerListView(ListView):
    model = Player
    template_name = 'playerslist.html'
    context_object_name = 'players'

#Remove a player from the original list 
class DeletePlayerView(DeleteView):
    model = Player
    template_name = 'playerdelete.html'
    context_object_name = 'player'
    success_url = reverse_lazy('playerslist')

    def delete(self,request,*args,**kwargs):
        messages.success(self.request,"Player removed successfully")
        return super().delete(request,*args,**kwargs)

#Update a player's detail(name, rating, position)
class UpdatePlayerView(UpdateView):
    model = Player
    form_class = PlayerCreationForm
    template_name = 'playerupdate.html'
    success_url = reverse_lazy('playerslist')

    def form_valid(self, form):
        messages.success(self.request, 'Player updated successfully')
        return super().form_valid(form)

# Reset all players

def reset_players(request):
    if request.method == 'POST':
        Player.objects.all().delete()
        messages.success(request, 'All players have been removed. Starting fresh!')
        return redirect('index')
    return render(request, 'reset_confirm.html')

#Snake Draft Algorithm
def generate_balanced_teams(player_ids,team_names):
    #Step1- Get the players by ratings (high to low)
    players = list(
        Player.objects.filter(id__in=player_ids)
        .order_by('-rating','position')
    )

    #Step2- Create empty teams
    teams = {name: [] for name in team_names}
    team_ratings = {name: 0 for name in team_names}

    #Distribute the players
    num_teams = len(team_names)

    for index,player in enumerate(players):
        iteration_number = index // num_teams
        position_in_iteration = index % num_teams

        if iteration_number % 2 == 1:
            position_in_iteration = num_teams - 1 - position_in_iteration

        team_name = team_names[position_in_iteration]
        teams[team_name].append(player)
        team_ratings[team_name] += player.rating
    return teams, team_ratings

def team_form_view(request):
    """Display the form to input team names and count"""
    player_count = Player.objects.count()
    return render(request, 'team_form.html', {'player_count': player_count})

def generate_teams_view(request):
    if request.method == 'POST':
        #GET the team names from the Form
        num_teams = int(request.POST.get('num_teams', 2))
        team_names = [
            request.POST.get(f'team_{i}_name', f'Team {i}').strip()
            for i in range(1, num_teams + 1)
        ]
        
        # Filter out any empty team names and ensure they're not None
        team_names = [name for name in team_names if name]
        
        if not team_names:
            messages.error(request, 'Please provide at least one team name.')
            return redirect('team_form')
        
        #Get the player ids for the snake draft algorithm
        player_ids = list(Player.objects.values_list('id', flat=True))
        
        if not player_ids:
            messages.error(request, 'No players available. Please add players first.')
            return redirect('playeradd')

        teams_dict, ratings = generate_balanced_teams(player_ids, team_names)
        #Clear old teams
        Team.objects.all().delete()
        Player.objects.update(team=None)

        for team_name, players in teams_dict.items():
            #Create a team
            team = Team.objects.create(name=team_name)

            for player in players:
                player.team = team
                player.save()
        
        messages.success(request, f'Created {len(team_names)} teams!')
        return redirect('teams_display')
    return redirect('team_form')

def teams_display_view(request):
    """Display the generated teams with their players"""
    teams = Team.objects.all().prefetch_related('players')
    
    # Calculate total and average ratings for each team
    teams_with_stats = []
    for team in teams:
        total_rating = sum(player.rating for player in team.players.all())
        player_count = team.players.count()
        avg_rating = total_rating / player_count if player_count > 0 else 0
        team.total_rating = total_rating
        team.avg_rating = avg_rating
        teams_with_stats.append(team)
    
    return render(request, 'teams_display.html', {'teams': teams_with_stats})

class RegisterView():
    pass