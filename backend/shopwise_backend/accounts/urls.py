# Core Imports
from django.urls import path

# Views
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenObtainPairView.as_view(), name='refresh_token'),

    # Profile and account management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('delete-account/', views.delete_account, name='delete-account'),

    # Email verification and password reset
    path('verify-email/', views.verify_email, name='verify-email'),
    path('password-reset/', views.RequestPasswordResetView.as_view(),
         name='password-reset'),
    path('logout/', views.logout_view, name='logout'),

]
