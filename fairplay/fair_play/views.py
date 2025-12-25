from django.shortcuts import render, redirect
from .forms import PlayerSearchForm, CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Player, Team, TeamMembership
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.utils import timezone

# Create your views here.
def index(request):
    """Main page view - redirect authenticated users to their player list"""
    if request.user.is_authenticated:
        return redirect('playerslist')
    return render(request, 'index.html')


@login_required
def add_player_view(request):
    if request.method == 'POST':
        form = PlayerSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                position = form.cleaned_data.get('position_override') or user.profile.preferred_position
                rating = form.cleaned_data.get('rating', 70)
                
                # Create player instance
                Player.objects.create(
                    user=user,
                    owner=request.user,
                    position=position,
                    rating=rating
                )
                messages.success(request, f'Added {username} to your team!')
                return redirect('playerslist')
            except User.DoesNotExist:
                messages.error(request, f'User "{username}" not found.')
    else:
        form = PlayerSearchForm()
    
    return render(request, 'playeradd.html', {'form': form})


class PlayerListView(LoginRequiredMixin, ListView):
    model = Player
    template_name = 'playerslist.html'
    context_object_name = 'players'
    
    def get_queryset(self):
        # Only show players owned by the current user
        return Player.objects.filter(owner=self.request.user)

#Remove a player from the original list 
class DeletePlayerView(LoginRequiredMixin, DeleteView):
    model = Player
    template_name = 'playerdelete.html'
    context_object_name = 'player'
    success_url = reverse_lazy('playerslist')
    
    def get_queryset(self):
        # Only allow deletion of own players
        return Player.objects.filter(
            Q(owner=self.request.user)|
            Q(team__owner = self.request.user)
        )

    def delete(self,request,*args,**kwargs):
        messages.success(self.request,"Player removed successfully")
        return super().delete(request,*args,**kwargs)

#Update a player's detail(name, rating, position)
class UpdatePlayerView(LoginRequiredMixin, UpdateView):
    model = Player
    fields = ['position', 'rating']
    template_name = 'playerupdate.html'
    success_url = reverse_lazy('playerslist')
    
    def get_queryset(self):
        # Only allow deletion of own players
        return Player.objects.filter(
            Q(owner=self.request.user)|
            Q(team__owner = self.request.user)
        )

    def form_valid(self, form):
        messages.success(self.request, 'Player updated successfully')
        return super().form_valid(form)

# Reset all players
@login_required
def reset_players(request):
    if request.method == 'POST':
        # Only delete current user's players
        Player.objects.filter(owner=request.user).delete()
        messages.success(request, 'All your players have been removed. Starting fresh!')
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

@login_required
def team_form_view(request):
    """Display the form to input team names and count"""
    player_count = Player.objects.filter(owner=request.user).count()
    return render(request, 'team_form.html', {'player_count': player_count})

@login_required
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
        
        #Get the player ids for the snake draft algorithm (only current user's players)
        player_ids = list(Player.objects.filter(owner=request.user).values_list('id', flat=True))
        
        if not player_ids:
            messages.error(request, 'No players available. Please add players first.')
            return redirect('playeradd')

        teams_dict, ratings = generate_balanced_teams(player_ids, team_names)
        
        #Clear old teams owned by current user
        Team.objects.filter(owner=request.user).delete()
        Player.objects.filter(owner=request.user).update(team=None)

        for team_name, players in teams_dict.items():
            #Create a team
            team = Team.objects.create(name=team_name, owner=request.user)

            #Add the owner as a member
            team.members.add(request.user)

            for player in players:
                player.team = team
                player.save()
                team.members.add(player.user)
        
        messages.success(request, f'Created {len(team_names)} teams!')
        return redirect('teams_display')
    return redirect('team_form')

@login_required
def teams_display_view(request):
    """Display the generated teams with their players"""
    owned_teams = Team.objects.filter(owner=request.user).prefetch_related('players', 'members')
    member_teams = Team.objects.filter(members=request.user).exclude(owner=request.user).prefetch_related('players', 'members', 'owner')
    
    # Calculate total and average ratings for each team
    teams_owned_with_stats = []
    for team in owned_teams:
        total_rating = sum(player.rating for player in team.players.all())
        count = team.players.count()
        team.total_rating = total_rating
        team.avg_rating = (total_rating / count) if count > 0 else 0
        teams_owned_with_stats.append(team)
    
    teams_member_with_stats = []
    for team in member_teams:
        total_rating = sum(player.rating for player in team.players.all())
        count = team.players.count()
        team.total_rating = total_rating
        team.avg_rating = (total_rating / count) if count > 0 else 0
        teams_member_with_stats.append(team)
    
    return render(request, 'teams_display.html', {
        'owned_teams': teams_owned_with_stats,
        'member_teams': teams_member_with_stats
    })


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('playerslist')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('playerslist')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('playerslist')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('playerslist')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')