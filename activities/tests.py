# activities/tests.py
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import DailyActivity

class DailyActivityTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test user
        self.user = User.objects.create_user(
            username='kobe',
            email='kobe@example.com',
            password='Password123!'
        )
        # Authenticate the user to get tokens
        response = self.client.post('/api/token/', {
            'username': 'kobe',
            'password': 'Password123!'
        }, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_daily_activity(self):
        """Test creating a new activity for an authenticated user"""
        url = '/api/activities/'
        data = {
            'title': 'Basketball',
            'description': '1 hour game full court'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyActivity.objects.count(), 1)
        self.assertEqual(DailyActivity.objects.first().title, 'Basketball')

    def test_unauthenticated_user_cannot_create_activity(self):
        """Test that an unauthenticated user cannot post"""
        self.client.credentials()  # remove the token
        url = '/api/activities/'
        data = {'title': 'Jogging', 'description': '30 minutes in the park'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_activities_for_authenticated_user(self):
        """Test that user can list their own activities"""
        # Create one activity
        DailyActivity.objects.create(user=self.user, title='Gym', description='Workout session')
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Gym')
