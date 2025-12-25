from django.shortcuts import render, redirect
from .forms import PlayerSearchForm, CustomUserCreationForm, MatchForm, MatchResultForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Player, Team, TeamMembership, Match, MatchParticipation
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404

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
        # Close all open memberships
        TeamMembership.objects.filter(
            player__owner=request.user,
            left_at__isnull=True
        ).update(left_at=timezone.now())
        
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
        
        # Close all current memberships before resetting teams
        TeamMembership.objects.filter(
            player__owner=request.user,
            left_at__isnull=True
        ).update(left_at=timezone.now())
        
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
                
                # Create new membership record
                TeamMembership.objects.create(
                    player=player,
                    team=team
                )
        
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


# ============= MATCH VIEWS =============

@login_required
def match_create_view(request):
    """Create/schedule a new match"""
    if request.method == 'POST':
        form = MatchForm(request.user, request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.save()
            
            # Auto-create participations for current team rosters
            for player in match.team_A.players.all():
                MatchParticipation.objects.create(
                    match=match,
                    team=match.team_A,
                    player=player
                )
            
            for player in match.team_B.players.all():
                MatchParticipation.objects.create(
                    match=match,
                    team=match.team_B,
                    player=player
                )
            
            messages.success(request, f'Match scheduled: {match.team_A} vs {match.team_B}')
            return redirect('match_list')
    else:
        form = MatchForm(request.user)
    
    return render(request, 'match_create.html', {'form': form})


@login_required
def match_list_view(request):
    """Display all matches for teams the user owns or is a member of"""
    # Get matches where user owns either team or is a member
    matches = Match.objects.filter(
        Q(team_A__owner=request.user) | 
        Q(team_B__owner=request.user) |
        Q(team_A__members=request.user) |
        Q(team_B__members=request.user)
    ).distinct().select_related('team_A', 'team_B').order_by('-played_at', '-date_created')
    
    # Separate by status
    upcoming = matches.filter(status=Match.Status.SCHEDULED)
    played = matches.filter(status=Match.Status.PLAYED)
    
    return render(request, 'match_list.html', {
        'upcoming_matches': upcoming,
        'played_matches': played
    })


@login_required
def match_detail_view(request, pk):
    """Display match details with rosters and participations"""
    match = get_object_or_404(
        Match.objects.select_related('team_A', 'team_B').prefetch_related(
            'participations__player__user',
            'team_A__players__user',
            'team_B__players__user'
        ),
        pk=pk
    )
    
    # Check if user has access to this match
    if not (match.team_A.owner == request.user or 
            match.team_B.owner == request.user or
            request.user in match.team_A.members.all() or
            request.user in match.team_B.members.all()):
        messages.error(request, 'You do not have access to this match.')
        return redirect('match_list')
    
    # Get participations grouped by team
    team_a_participations = match.participations.filter(team=match.team_A).select_related('player__user')
    team_b_participations = match.participations.filter(team=match.team_B).select_related('player__user')
    
    context = {
        'match': match,
        'team_a_participations': team_a_participations,
        'team_b_participations': team_b_participations,
        'can_edit': match.team_A.owner == request.user or match.team_B.owner == request.user
    }
    
    return render(request, 'match_detail.html', context)


@login_required
def match_record_result_view(request, pk):
    """Record the result of a match"""
    match = get_object_or_404(Match, pk=pk)
    
    # Only team owners can record results
    if match.team_A.owner != request.user and match.team_B.owner != request.user:
        messages.error(request, 'Only team owners can record match results.')
        return redirect('match_detail', pk=pk)
    
    if request.method == 'POST':
        form = MatchResultForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            messages.success(request, f'Result recorded: {match}')
            return redirect('match_detail', pk=pk)
    else:
        form = MatchResultForm(instance=match)
    
    return render(request, 'match_record_result.html', {
        'form': form,
        'match': match
    })


# ============= HISTORY VIEWS =============

@login_required
def my_history_view(request):
    """Show user's participation history across all teams and matches"""
    # Get all players associated with this user
    user_players = Player.objects.filter(user=request.user)
    
    # Get all team memberships (current and past)
    memberships = TeamMembership.objects.filter(
        player__user=request.user
    ).select_related('team', 'player').order_by('-joined_at')
    
    # Get all match participations
    participations = MatchParticipation.objects.filter(
        player__user=request.user
    ).select_related('match__team_A', 'match__team_B', 'team', 'player').order_by('-match__played_at', '-match__date_created')
    
    # Calculate stats
    total_matches = participations.count()
    total_goals = sum(p.goals for p in participations)
    total_assists = sum(p.assists for p in participations)
    
    # Count wins/draws/losses
    wins = 0
    draws = 0
    losses = 0
    
    for participation in participations:
        if participation.match.status == Match.Status.PLAYED:
            winner = participation.match.winner
            if winner == participation.team:
                wins += 1
            elif winner is None:
                draws += 1
            else:
                losses += 1
    
    context = {
        'memberships': memberships,
        'participations': participations,
        'stats': {
            'total_matches': total_matches,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals': total_goals,
            'assists': total_assists
        }
    }
    
    return render(request, 'my_history.html', context)


@login_required
def team_history_view(request, team_id):
    """Show team's history including matches and membership changes"""
    team = get_object_or_404(Team, pk=team_id)
    
    # Check if user has access
    if team.owner != request.user and request.user not in team.members.all():
        messages.error(request, 'You do not have access to this team.')
        return redirect('teams_display')
    
    # Get all matches involving this team
    matches = Match.objects.filter(
        Q(team_A=team) | Q(team_B=team)
    ).select_related('team_A', 'team_B').order_by('-played_at', '-date_created')
    
    # Get membership history
    memberships = TeamMembership.objects.filter(
        team=team
    ).select_related('player__user').order_by('-joined_at')
    
    # Calculate team stats
    wins = 0
    draws = 0
    losses = 0
    goals_for = 0
    goals_against = 0
    
    for match in matches:
        if match.status == Match.Status.PLAYED and match.score_a is not None and match.score_b is not None:
            if match.team_A == team:
                goals_for += match.score_a
                goals_against += match.score_b
                if match.score_a > match.score_b:
                    wins += 1
                elif match.score_a < match.score_b:
                    losses += 1
                else:
                    draws += 1
            else:  # team_B
                goals_for += match.score_b
                goals_against += match.score_a
                if match.score_b > match.score_a:
                    wins += 1
                elif match.score_b < match.score_a:
                    losses += 1
                else:
                    draws += 1
    
    context = {
        'team': team,
        'matches': matches,
        'memberships': memberships,
        'stats': {
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'total_matches': wins + draws + losses
        }
    }
    
    return render(request, 'team_history.html', context)