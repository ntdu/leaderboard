from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user_manager = self.user_model.objects

    def test_create_user_with_valid_data(self):
        user = self.user_manager.create_user(
            email='testuser@example.com',
            user_name='testuser',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.user_name, 'testuser')
        self.assertTrue(user.check_password('testpassword123'))

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as context:
            self.user_manager.create_user(
                email='',
                user_name='testuser',
                password='testpassword123'
            )
        self.assertEqual(str(context.exception), 'Provide email')
