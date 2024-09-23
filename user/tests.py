from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from .models import CustomUser

class CustomUserModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='testpassword',
            user_role='Coach'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.user_role, 'Coach')
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'Test User (testuser@example.com)')

    def test_default_user_role(self):
        default_user = CustomUser.objects.create_user(
            username='defaultuser',
            first_name='Default',
            last_name='User',
            email='defaultuser@example.com',
            password='defaultpassword'
        )
        self.assertEqual(default_user.user_role, 'Coach')

    def test_user_role_choices(self):
        agent_user = CustomUser.objects.create_user(
            username='agentuser',
            first_name='Agent',
            last_name='User',
            email='agentuser@example.com',
            password='agentpassword',
            user_role='Agent'
        )
        self.assertEqual(agent_user.user_role, 'Agent')

    def test_update_timestamp(self):
        old_updated_at = self.user.updated_at
        self.user.first_name = 'Updated'
        self.user.save()
        self.assertNotEqual(old_updated_at, self.user.updated_at)
        self.assertTrue(self.user.updated_at > old_updated_at)