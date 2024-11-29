from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
    """Custom user model for authentication using email."""

    # User model fields
    email = models.EmailField(_('email address'), unique=True)
    postal_code = models.CharField(max_length=5, blank=True)
    suburb = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Email verification tokens
    email_verification_token = models.CharField(max_length=255, blank=True)
    email_verification_token_expires = models.DateTimeField(null=True)

    # Verification fields
    created_at = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'

    # Required fields for user model
    REQUIRED_FIELDS = ['username']
    # Meta data for user model

    class Meta:
        db_table = 'users' 
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    # Delete the user account
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
