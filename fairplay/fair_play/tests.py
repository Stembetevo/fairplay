from django.test import TestCase, Client
from django.urls import reverse
from .models import Player, Team, Match
from .forms import PlayerCreationForm, TeamForm
from django.core.exceptions import ValidationError


class PlayerModelTest(TestCase):
    """Test cases for the Player model"""
    
    def setUp(self):
        """Set up test data"""
        self.team = Team.objects.create(name="Test Team")
        self.player = Player.objects.create(
            name="John Doe",
            position=Player.Position.ST,
            rating=4,
            team=self.team
        )
    
    def test_player_creation(self):
        """Test that a player can be created successfully"""
        self.assertEqual(self.player.name, "John Doe")
        self.assertEqual(self.player.position, "Striker")
        self.assertEqual(self.player.rating, 4)
        self.assertEqual(self.player.team, self.team)
    
    def test_player_str_method(self):
        """Test the string representation of a player"""
        expected = "John Doe (Rating: 4)"
        self.assertEqual(str(self.player), expected)
    
    def test_player_default_rating(self):
        """Test that the default rating is 3"""
        player = Player.objects.create(
            name="Jane Smith",
            position=Player.Position.GK
        )
        self.assertEqual(player.rating, 3)
    
    def test_player_rating_validation(self):
        """Test that rating validation works (50-100 range)"""
        # Valid ratings should work
        for rating in range(50, 100):
            player = Player(
                name=f"Player {rating}",
                position=Player.Position.MD,
                rating=rating
            )
            player.full_clean()  # Should not raise
        
        # Invalid ratings should fail
        invalid_player = Player(
            name="Invalid Player",
            position=Player.Position.DF,
            rating=60
        )
        with self.assertRaises(ValidationError):
            invalid_player.full_clean()
    
    def test_player_ordering(self):
        """Test that players are ordered by name"""
        Player.objects.create(name="Zara", position=Player.Position.ST, rating=3)
        Player.objects.create(name="Adam", position=Player.Position.DF, rating=4)
        
        players = list(Player.objects.all())
        self.assertEqual(players[0].name, "Adam")
        self.assertEqual(players[2].name, "Zara")


class TeamModelTest(TestCase):
    """Test cases for the Team model"""
    
    def test_team_creation(self):
        """Test that a team can be created successfully"""
        team = Team.objects.create(name="Warriors")
        self.assertEqual(team.name, "Warriors")
        self.assertIsNotNone(team.created_at)
    
    def test_team_str_method(self):
        """Test the string representation of a team"""
        team = Team.objects.create(name="Champions")
        self.assertEqual(str(team), "Champions")
    
    def test_team_player_relationship(self):
        """Test the relationship between team and players"""
        team = Team.objects.create(name="Eagles")
        player1 = Player.objects.create(name="Player 1", position=Player.Position.ST, team=team)
        player2 = Player.objects.create(name="Player 2", position=Player.Position.GK, team=team)
        
        self.assertEqual(team.players.count(), 2)
        self.assertIn(player1, team.players.all())
        self.assertIn(player2, team.players.all())
    
    def test_team_ordering(self):
        """Test that teams are ordered by name"""
        Team.objects.create(name="Zebras")
        Team.objects.create(name="Ants")
        
        teams = list(Team.objects.all())
        self.assertEqual(teams[0].name, "Ants")
        self.assertEqual(teams[1].name, "Zebras")


class MatchModelTest(TestCase):
    """Test cases for the Match model"""
    
    def setUp(self):
        """Set up test data"""
        self.team_a = Team.objects.create(name="Team A")
        self.team_b = Team.objects.create(name="Team B")
    
    def test_match_creation(self):
        """Test that a match can be created successfully"""
        match = Match.objects.create(team_A=self.team_a, team_B=self.team_b)
        self.assertEqual(match.team_A, self.team_a)
        self.assertEqual(match.team_B, self.team_b)
        self.assertIsNotNone(match.date_created)
    
    def test_match_str_method(self):
        """Test the string representation of a match"""
        match = Match.objects.create(team_A=self.team_a, team_B=self.team_b)
        expected = f"{self.team_a.name} vs {self.team_b.name}"
        self.assertEqual(str(match), expected)


class PlayerCreationFormTest(TestCase):
    """Test cases for the PlayerCreationForm"""
    
    def test_valid_form(self):
        """Test that a valid form passes validation"""
        form_data = {
            'name': 'Test Player',
            'position': Player.Position.ST,
            'rating': 4
        }
        form = PlayerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_rating_too_high(self):
        """Test that rating above 5 is invalid"""
        form_data = {
            'name': 'Test Player',
            'position': Player.Position.ST,
            'rating': 6
        }
        form = PlayerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_rating_too_low(self):
        """Test that rating below 1 is invalid"""
        form_data = {
            'name': 'Test Player',
            'position': Player.Position.ST,
            'rating': 0
        }
        form = PlayerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_empty_name(self):
        """Test that empty name is invalid"""
        form_data = {
            'name': '',
            'position': Player.Position.ST,
            'rating': 3
        }
        form = PlayerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        self.player1 = Player.objects.create(
            name="Player 1",
            position=Player.Position.ST,
            rating=5
        )
        self.player2 = Player.objects.create(
            name="Player 2",
            position=Player.Position.GK,
            rating=3
        )
    
    def test_index_view(self):
        """Test the index page loads successfully"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_player_list_view(self):
        """Test the player list view"""
        response = self.client.get(reverse('playerslist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'playerslist.html')
        self.assertContains(response, "Player 1")
        self.assertContains(response, "Player 2")
    
    def test_create_player_view_get(self):
        """Test GET request to create player view"""
        response = self.client.get(reverse('playeradd'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'playeradd.html')
    
    def test_create_player_view_post(self):
        """Test POST request to create a new player"""
        player_count_before = Player.objects.count()
        response = self.client.post(reverse('playeradd'), {
            'name': 'New Player',
            'position': Player.Position.MD,
            'rating': 4
        })
        self.assertEqual(Player.objects.count(), player_count_before + 1)
        self.assertRedirects(response, reverse('playerslist'))
        
        # Check the player was created
        new_player = Player.objects.get(name='New Player')
        self.assertEqual(new_player.rating, 4)
    
    def test_update_player_view_get(self):
        """Test GET request to update player view"""
        response = self.client.get(reverse('playerupdate', kwargs={'pk': self.player1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'playerupdate.html')
    
    def test_update_player_view_post(self):
        """Test POST request to update a player"""
        response = self.client.post(reverse('playerupdate', kwargs={'pk': self.player1.pk}), {
            'name': 'Updated Player',
            'position': Player.Position.DF,
            'rating': 5
        })
        self.assertRedirects(response, reverse('playerslist'))
        
        # Check the player was updated
        self.player1.refresh_from_db()
        self.assertEqual(self.player1.name, 'Updated Player')
        self.assertEqual(self.player1.position, 'Defender')
    
    def test_delete_player_view_get(self):
        """Test GET request to delete player confirmation"""
        response = self.client.get(reverse('playerdelete', kwargs={'pk': self.player1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'playerdelete.html')
    
    def test_delete_player_view_post(self):
        """Test POST request to delete a player"""
        player_count_before = Player.objects.count()
        response = self.client.post(reverse('playerdelete', kwargs={'pk': self.player1.pk}))
        self.assertEqual(Player.objects.count(), player_count_before - 1)
        self.assertRedirects(response, reverse('playerslist'))
        
        # Check the player was deleted
        with self.assertRaises(Player.DoesNotExist):
            Player.objects.get(pk=self.player1.pk)
    
    def test_reset_players_view_get(self):
        """Test GET request to reset players confirmation"""
        response = self.client.get(reverse('reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reset_confirm.html')
    
    def test_reset_players_view_post(self):
        """Test POST request to reset all players"""
        self.assertGreater(Player.objects.count(), 0)
        response = self.client.post(reverse('reset'))
        self.assertEqual(Player.objects.count(), 0)
        self.assertRedirects(response, reverse('index'))
    
    def test_team_form_view(self):
        """Test the team form view"""
        response = self.client.get(reverse('team_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team_form.html')
        self.assertIn('player_count', response.context)
    
    def test_teams_display_view(self):
        """Test the teams display view"""
        # Create some teams with players
        team = Team.objects.create(name="Test Team")
        self.player1.team = team
        self.player1.save()
        
        response = self.client.get(reverse('teams_display'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams_display.html')
        self.assertIn('teams', response.context)


class BalancedTeamsGenerationTest(TestCase):
    """Test cases for the balanced team generation algorithm"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        # Create players with different ratings
        self.players = [
            Player.objects.create(name=f"Player {i}", position=Player.Position.ST, rating=5-i%5)
            for i in range(10)
        ]
    
    def test_generate_teams_with_no_players(self):
        """Test team generation with no players"""
        Player.objects.all().delete()
        response = self.client.post(reverse('generate_teams'), {
            'num_teams': 2,
            'team_1_name': 'Team A',
            'team_2_name': 'Team B',
        })
        self.assertRedirects(response, reverse('playeradd'))
    
    def test_generate_teams_with_valid_data(self):
        """Test team generation with valid data"""
        response = self.client.post(reverse('generate_teams'), {
            'num_teams': 2,
            'team_1_name': 'Warriors',
            'team_2_name': 'Champions',
        })
        self.assertRedirects(response, reverse('teams_display'))
        
        # Check that teams were created
        self.assertEqual(Team.objects.count(), 2)
        
        # Check that all players are assigned to teams
        unassigned_players = Player.objects.filter(team=None).count()
        self.assertEqual(unassigned_players, 0)
    
    def test_balanced_team_ratings(self):
        """Test that teams are balanced in terms of ratings"""
        self.client.post(reverse('generate_teams'), {
            'num_teams': 2,
            'team_1_name': 'Team A',
            'team_2_name': 'Team B',
        })
        
        teams = Team.objects.all()
        ratings = []
        for team in teams:
            total_rating = sum(player.rating for player in team.players.all())
            ratings.append(total_rating)
        
        # Check that the ratings are relatively balanced (difference should be small)
        rating_difference = abs(ratings[0] - ratings[1])
        self.assertLessEqual(rating_difference, 5)  # Allow some variance
    
    def test_generate_multiple_teams(self):
        """Test generating more than 2 teams"""
        # Create more players for better distribution
        for i in range(10, 20):
            Player.objects.create(name=f"Player {i}", position=Player.Position.MD, rating=3)
        
        response = self.client.post(reverse('generate_teams'), {
            'num_teams': 4,
            'team_1_name': 'Team 1',
            'team_2_name': 'Team 2',
            'team_3_name': 'Team 3',
            'team_4_name': 'Team 4',
        })
        self.assertRedirects(response, reverse('teams_display'))
        
        # Check that 4 teams were created
        self.assertEqual(Team.objects.count(), 4)
        
        # Check that all players are distributed
        for team in Team.objects.all():
            self.assertGreater(team.players.count(), 0)
    
    def test_teams_cleared_before_generation(self):
        """Test that old teams are cleared before generating new ones"""
        # Create initial teams
        Team.objects.create(name="Old Team")
        
        response = self.client.post(reverse('generate_teams'), {
            'num_teams': 2,
            'team_1_name': 'New Team A',
            'team_2_name': 'New Team B',
        })
        
        # Check that old teams are gone and only new teams exist
        self.assertEqual(Team.objects.count(), 2)
        self.assertFalse(Team.objects.filter(name="Old Team").exists())
        self.assertTrue(Team.objects.filter(name="New Team A").exists())
