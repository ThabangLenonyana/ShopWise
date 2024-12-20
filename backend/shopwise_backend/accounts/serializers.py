# Core Imports
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Authentication
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

# Documentation and API schema with OpenAPI Swagger Tools
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

User = get_user_model()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid Login Response',
            value={
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                'user': {
                    'id': 1,
                    'email': 'user@example.com',
                    'username': 'testuser',
                    'first_name': 'John',
                    'last_name': 'Doe'
                }
            }
        )
    ]
)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for JWT token generation with additional user info."""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra responses
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name
        }

        return data


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid User Registration',
            value={
                'email': 'user@example.com',
                'username': 'testuser',
                'password': 'SecurePass123!',
                'password2': 'SecurePass123!',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
    ]
)
class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration and management."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2',
                  )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def validate(self, attrs):
        """Validate passwords match."""

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """Create and return a new user."""

        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Update and return an existing user."""
        validated_data.pop('password2', None)

        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data.get('password'))

        return super().update(instance, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'avatar', 'postal_code', 'suburb', 'phone_number')
        read_only_fields = ('email',)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(
        min_length=8, validators=[validate_password], write_only=True)
