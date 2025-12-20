from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Player, Team


class TeamMembershipViewTests(TestCase):
    """Tests for owned teams vs member teams display"""
    
    def setUp(self):
        """Set up test users and client"""
        self.client = Client()
        
        # Create test users
        self.user1 = User.objects.create_user(username='alice', password='test123')
        self.user2 = User.objects.create_user(username='bob', password='test123')
        self.user3 = User.objects.create_user(username='charlie', password='test123')
        
    def test_owned_teams_displayed_in_correct_section(self):
        """Test that teams created by user appear in owned teams section"""
        self.client.login(username='alice', password='test123')
        
        # Create team owned by alice
        team = Team.objects.create(name='Team Alpha', owner=self.user1)
        team.members.add(self.user1)
        
        response = self.client.get(reverse('teams_display'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('owned_teams', response.context)
        self.assertEqual(len(response.context['owned_teams']), 1)
        self.assertEqual(response.context['owned_teams'][0].name, 'Team Alpha')
        
    def test_member_teams_displayed_separately(self):
        """Test that teams where user is member (not owner) appear in member teams section"""
        self.client.login(username='bob', password='test123')
        
        # Create team owned by alice, add bob as member
        team = Team.objects.create(name='Team Beta', owner=self.user1)
        team.members.add(self.user1)
        team.members.add(self.user2)  # bob is member
        
        response = self.client.get(reverse('teams_display'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('member_teams', response.context)
        self.assertEqual(len(response.context['member_teams']), 1)
        self.assertEqual(response.context['member_teams'][0].name, 'Team Beta')
        self.assertEqual(len(response.context['owned_teams']), 0)  # bob owns no teams
        
    def test_owned_teams_exclude_from_member_teams(self):
        """Test that owned teams don't appear in member teams section"""
        self.client.login(username='alice', password='test123')
        
        # Create team owned by alice
        team = Team.objects.create(name='Team Gamma', owner=self.user1)
        team.members.add(self.user1)  # alice is both owner and member
        
        response = self.client.get(reverse('teams_display'))
        
        # Should appear in owned, not in member
        self.assertEqual(len(response.context['owned_teams']), 1)
        self.assertEqual(len(response.context['member_teams']), 0)
        
    def test_multiple_teams_separated_correctly(self):
        """Test user with both owned and member teams sees correct separation"""
        self.client.login(username='charlie', password='test123')
        
        # Charlie owns 2 teams
        team1 = Team.objects.create(name='Charlie Team 1', owner=self.user3)
        team1.members.add(self.user3)
        team2 = Team.objects.create(name='Charlie Team 2', owner=self.user3)
        team2.members.add(self.user3)
        
        # Charlie is member of 3 other teams
        team3 = Team.objects.create(name='Alice Team', owner=self.user1)
        team3.members.add(self.user1, self.user3)
        
        team4 = Team.objects.create(name='Bob Team 1', owner=self.user2)
        team4.members.add(self.user2, self.user3)
        
        team5 = Team.objects.create(name='Bob Team 2', owner=self.user2)
        team5.members.add(self.user2, self.user3)
        
        response = self.client.get(reverse('teams_display'))
        
        self.assertEqual(len(response.context['owned_teams']), 2)
        self.assertEqual(len(response.context['member_teams']), 3)
        
    def test_team_generation_adds_members_automatically(self):
        """Test that generating teams automatically adds player users as members"""
        self.client.login(username='alice', password='test123')
        
        # Add players for alice
        Player.objects.create(user=self.user1, owner=self.user1, position='Striker', rating=80)
        Player.objects.create(user=self.user2, owner=self.user1, position='Defender', rating=75)
        Player.objects.create(user=self.user3, owner=self.user1, position='MidFielder', rating=85)
        
        # Generate teams
        response = self.client.post(reverse('generate_teams'), {
            'num_teams': 2,
            'team_1_name': 'Red Team',
            'team_2_name': 'Blue Team'
        })
        
        # Check that teams were created
        teams = Team.objects.filter(owner=self.user1)
        self.assertEqual(teams.count(), 2)
        
        # Check that members were added
        for team in teams:
            # Owner should be a member
            self.assertIn(self.user1, team.members.all())
            # Players assigned to this team should be members
            for player in team.players.all():
                self.assertIn(player.user, team.members.all())
                
    def test_member_can_view_team_but_sees_owner_name(self):
        """Test that member teams display shows the owner's username"""
        self.client.login(username='bob', password='test123')
        
        # Alice creates team with bob as member
        team = Team.objects.create(name='Exclusive Team', owner=self.user1)
        team.members.add(self.user1, self.user2)
        
        response = self.client.get(reverse('teams_display'))
        
        # Bob should see it in member teams
        self.assertEqual(len(response.context['member_teams']), 1)
        member_team = response.context['member_teams'][0]
        self.assertEqual(member_team.owner, self.user1)
        
    def test_empty_teams_display_correctly(self):
        """Test that users with no teams see appropriate placeholders"""
        self.client.login(username='charlie', password='test123')
        
        response = self.client.get(reverse('teams_display'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['owned_teams']), 0)
        self.assertEqual(len(response.context['member_teams']), 0)
        self.assertContains(response, 'No teams created yet')
        self.assertContains(response, 'Not added to any teams yet')
        
    def test_team_stats_calculated_for_both_sections(self):
        """Test that total_rating and avg_rating are calculated for owned and member teams"""
        self.client.login(username='alice', password='test123')
        
        # Create owned team with players
        owned_team = Team.objects.create(name='Owned Team', owner=self.user1)
        owned_team.members.add(self.user1)
        p1 = Player.objects.create(user=self.user1, owner=self.user1, position='Striker', rating=80, team=owned_team)
        p2 = Player.objects.create(user=self.user2, owner=self.user1, position='Defender', rating=70, team=owned_team)
        
        # Create member team with players
        member_team = Team.objects.create(name='Member Team', owner=self.user2)
        member_team.members.add(self.user1, self.user2)
        p3 = Player.objects.create(user=self.user1, owner=self.user2, position='MidFielder', rating=90, team=member_team)
        
        response = self.client.get(reverse('teams_display'))
        
        # Check owned team stats
        owned = response.context['owned_teams'][0]
        self.assertEqual(owned.total_rating, 150)  # 80 + 70
        self.assertEqual(owned.avg_rating, 75.0)   # 150 / 2
        
        # Check member team stats
        member = response.context['member_teams'][0]
        self.assertEqual(member.total_rating, 90)
        self.assertEqual(member.avg_rating, 90.0)