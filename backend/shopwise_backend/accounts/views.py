# Core Imports
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import get_user_model

# Authentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import logout

# Serializers
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,)

# Services
from .services.email import EmailService

# Documentation and API schema with OpenAPI Swagger Tools
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        description='Login to obtain JWT tokens',
        responses={
            200: OpenApiResponse(
                description='Login successful',
                response=CustomTokenObtainPairSerializer
            ),
            401: OpenApiResponse(description='Invalid credentials')
        },
        tags=['authentication'],
        summary='Login user and obtain tokens'
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Register view


class RegisterView(generics.CreateAPIView):
    """ Register new user """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        description='Register a new user account',
        request=UserSerializer,
        responses={
            201: OpenApiResponse(
                description='User created successfully',
                response=UserSerializer
            ),
            400: OpenApiResponse(
                description='Invalid input',
                examples=[
                    OpenApiExample(
                        'Password Mismatch',
                        value={'password': ["Password fields didn't match."]}
                    ),
                    OpenApiExample(
                        'Email Exists',
                        value={
                            'email': ["User with this email already exists."]}
                    )
                ]
            )
        },
        tags=['authentication'],
        summary='Create new user account',
        operation_id='register_user'
    )
    def post(self, request, *args, **kwargs):
        """
        Register a new user with email, username, and password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        email_service = EmailService()
        email_service.send_verification_email(user)

        return Response({
            "user": UserSerializer(user).data,
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)

# Profile view


class UserProfileView(generics.RetrieveUpdateAPIView):
    """ User profile view """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Password reset view


class RequestPasswordResetView(generics.GenericAPIView):
    """ Request password reset """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            token = default_token_generator.make_token(user)
            EmailService.send_password_reset_email(user, token)
            return Response({'message': 'Password reset email sent'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User with this email does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

# Email verification view


@api_view(['POST'])
def verify_email(request):
    """ Verify user email """
    token = request.data.get('token')
    try:
        user = User.objects.get(
            email_verification_token=token,
            email_verification_token_expires__gt=timezone.now(),
            is_email_verified=False
        )
        user.is_email_verified = True
        user.email_verification_token = ''
        user.save()
        return Response({'message': 'Email verified successfully'})
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid or expired token'},
            status=status.HTTP_400_BAD_REQUEST
        )

# Logout


@api_view(['POST'])
def logout_view(request):
    """ Logout user """
    logout(request)
    return Response({'message': 'Logged out successfully'})

# Account deletion


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """ Soft delete user account """
    user = request.user
    user.soft_delete()
    return Response({'message': 'Account deleted successfully'})
