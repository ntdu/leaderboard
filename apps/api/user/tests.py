
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTests(APITestCase):
    def test_registration(self):
        url = reverse('api:registration')
        data = {
            'user_name': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('response', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_registration_missing_fields(self):
        url = reverse('api:registration')
        data = {
            'user_name': 'testuser',
            'email': 'testuser@example.com',
            # Missing password fields
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['message'])
        self.assertIn('password2', response.data['message'])

    def test_registration_mismatched_passwords(self):
        url = reverse('api:registration')
        data = {
            'user_name': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'password2': 'differentpassword'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_invalid_email(self):
        url = reverse('api:registration')
        data = {
            'user_name': 'testuser',
            'email': 'invalid-email',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['message'])

    def test_registration_existing_user(self):
        get_user_model().objects.create_user(
            user_name='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        url = reverse('api:registration')
        data = {
            'user_name': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_name', response.data['message'])
        self.assertIn('email', response.data['message'])

class UserDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            user_name='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.login_url = reverse('api:token_obtain_pair')
        self.me_url = reverse('api:user-detail')

    def test_get_user_details_with_token(self):
        # Log in to obtain the token
        login_data = {
            'user_name': 'testuser',
            'password': 'testpassword123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(login_response.status_code, 200)
        token = login_response.data['access']

        # Add the token to the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Make the request to the /me endpoint
        response = self.client.get(self.me_url)

        # Check the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user_name'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['id'], self.user.id)
