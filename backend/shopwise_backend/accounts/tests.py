# Core Imports
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

# Test Suites
from django.test import TestCase
from rest_framework.test import APITestCase

# Models
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

    def test_email_verification(self):
        """Test email verification process."""

        # Create unverified user
        user = User.objects.create_user(
            username='unverified',
            email='unverified@example.com',
            password='TestPass123!',
            first_name='Unverified',
            last_name='User'
        )
        self.assertFalse(user.is_email_verified)

        # Mock email verification token
        user.email_verification_token = 'test-token'
        user.email_verification_token_expires = timezone.now() + timedelta(hours=24)
        user.save()

        # Test verification endpoint
        verify_url = reverse('verify-email')
        response = self.client.post(verify_url, {'token': 'test-token'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_email_verified)

    def test_password_reset_request(self):
        """Test password reset request flow."""
        # Request password reset
        reset_request_url = reverse('password-reset')
        response = self.client.post(reset_request_url, {
            'email': self.test_user.email
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_verification_invalid_token(self):
        """Test email verification with invalid token."""
        verify_url = reverse('verify-email')
        response = self.client.post(verify_url, {'token': 'invalid-token'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_invalid_email(self):
        """Test password reset request with non-existent email."""
        reset_request_url = reverse('password-reset')
        response = self.client.post(reset_request_url, {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
