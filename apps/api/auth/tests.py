from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class AuthViewTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            user_name='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token_obtain_url = reverse('api:token_obtain_pair')
        self.token_refresh_url = reverse('api:token_refresh')
        self.logout_url = reverse('api:logout')

    def test_obtain_token(self):
        data = {
            'user_name': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.token_obtain_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user_name', response.data)
        self.assertIn('email', response.data)

    def test_obtain_token_with_email(self):
        data = {
            'user_name': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.token_obtain_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user_name', response.data)
        self.assertIn('email', response.data)

    def test_invalid_login(self):
        data = {
            'user_name': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_obtain_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        # Obtain token first
        data = {
            'user_name': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.token_obtain_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        # Refresh token
        refresh_data = {
            'refresh': refresh_token
        }
        response = self.client.post(self.token_refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_invalid_refresh_token(self):
        refresh_data = {
            'refresh': 'invalidtoken'
        }
        response = self.client.post(self.token_refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_blacklist_token(self):
        # Obtain token first
        data = {
            'user_name': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.token_obtain_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.data['refresh']

        # Logout (blacklist token)
        logout_data = {
            'refresh': refresh_token
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
        response = self.client.post(self.logout_url, logout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_invalid_token(self):
        logout_data = {
            'refresh': 'invalidtoken'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.post(self.logout_url, logout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
