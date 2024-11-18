# accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class AuthenticationTests(APITestCase):
    """Test suite for authentication functionality."""

    def setUp(self):
        """Create test user."""
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_token_url = reverse('refresh_token')

    def test_user_registration(self):
        """Test user registration endpoint."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'NewPass123!',
            'password2': 'NewPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertIn('user', response.data)
        self.assertIn('message', response.data)

    def test_user_registration_invalid_password(self):
        """Test registration with non-matching passwords."""
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'NewPass123!',
            'password2': 'DifferentPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Test user login and token generation."""
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123!'
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'WrongPass123!'
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserModelTests(TestCase):
    """Test suite for User model."""

    def test_create_user(self):
        """Test creating a new user."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('TestPass123!'))
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_user_str_method(self):
        """Test the string representation of User model."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )

        self.assertEqual(str(user), 'test@example.com')


class UserSerializerTests(TestCase):
    """Test suite for User serializer."""

    def test_password_validation(self):
        """Test password validation in UserSerializer."""
        from .serializers import UserSerializer

        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'weak',  # Too weak password
            'password2': 'weak',
            'first_name': 'Test',
            'last_name': 'User'
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
