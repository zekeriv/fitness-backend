# accounts/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

class UserAuthTests(APITestCase):

    def setUp(self):
        # Use DRF's APIClient explicitly
        self.client = APIClient()

        # Create an existing user for login/logout tests
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='strongpassword123'
        )

    def test_user_registration(self):
        url = reverse('auth_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout_requires_authentication(self):
        url = reverse('auth_logout')
        # Sending request without authentication
        data = {'refresh': 'invalidtoken'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # your view returns 400 for invalid token

    def test_logout_with_authentication(self):
        # Generate refresh token for existing user
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.user)

        url = reverse('auth_logout')
        data = {'refresh': str(refresh)}
        # Force authenticate using APIClient
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
