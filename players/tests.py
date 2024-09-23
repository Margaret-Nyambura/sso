from django.test import TestCase
from django.utils import timezone
from .models import Team, Players
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='coachuser',
            email='coachuser@example.com',
            password='testpassword'
        )
        self.team = Team.objects.create(
            name='Kipaji',
            coach=self.user
        )

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Kipaji')
        self.assertEqual(self.team.coach, self.user)

    def test_team_string_representation(self):
        self.assertEqual(str(self.team), 'Kipaji')


class PlayersModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='coachuser',
            email='coachuser@example.com',
            password='testpassword'
        )
        self.team = Team.objects.create(
            name='Kipaji',
            coach=self.user
        )
        self.player = Players.objects.create(
            name='John Doe',
            date_of_birth=timezone.now(),
            team=self.team,
            position='Striker'
        )

    def test_player_creation(self):
        self.assertEqual(self.player.name, 'John Doe')
        self.assertEqual(self.player.team, self.team)
        self.assertEqual(self.player.position, 'Striker')

    def test_player_string_representation(self):
        self.assertEqual(str(self.player), 'John Doe')

    def test_position_choices(self):
        for position in Players.POSITION_CHOICES:
            self.assertIn(position[0], ['Goalkeeper', 'Defender', 'Striker'])

    def test_team_relationship(self):
        self.assertIn(self.player, self.team.players.all())