from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

class UserAdminTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser('admin', 'adminpassword')
        self.client.login(username='admin', password='adminpassword')
        self.user_to_delete = get_user_model().objects.create_user(username='user_to_delete', password='password')

    def test_delete_user(self):
        self.assertTrue(get_user_model().objects.filter(username='user_to_delete').exists())
        response = self.client.delete(f'/api/users/{self.user_to_delete.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(get_user_model().objects.filter(username='user_to_delete').exists())