from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample


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


class RegisterView(generics.CreateAPIView):
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
        return Response({
            "user": UserSerializer(user).data,
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)
