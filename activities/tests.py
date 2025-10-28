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
        # Create a sample activity
        self.activity = DailyActivity.objects.create(
            user=self.user,
            title='Morning Run',
            description='Ran 5km in the park',
            status='planned'
        )

    def test_create_daily_activity(self):
        """Test creating a new activity for an authenticated user"""
        url = '/api/activities/'
        data = {
            'title': 'Basketball',
            'description': '1 hour game full court',
            'status': 'in_progress'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyActivity.objects.count(), 2)
        self.assertEqual(DailyActivity.objects.last().title, 'Basketball')

    def test_unauthenticated_user_cannot_create_activity(self):
        """Test that an unauthenticated user cannot post"""
        self.client.credentials()  # remove the token
        url = '/api/activities/'
        data = {'title': 'Jogging', 'description': '30 minutes in the park'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_activities_for_authenticated_user(self):
        """Test that user can list their own activities"""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Morning Run')

    def test_retrieve_activity(self):
        """Test retrieving a single activity"""
        url = f'/api/activities/{self.activity.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Morning Run')

    def test_update_activity_status(self):
        """Test updating the status of an activity"""
        url = f'/api/activities/{self.activity.id}/'
        data = {'status': 'completed'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.activity.refresh_from_db()
        self.assertEqual(self.activity.status, 'completed')

    def test_delete_activity(self):
        """Test deleting an activity"""
        url = f'/api/activities/{self.activity.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DailyActivity.objects.filter(id=self.activity.id).exists())
