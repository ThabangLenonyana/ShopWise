from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta


class EmailService:
    """Service class for sending emails."""

    @staticmethod
    def send_verification_email(user):
        """Send email verification link to the user."""

        # Generate email verification token
        token = get_random_string(length=32)
        user.email_verification_token = token
        user.email_verification_token_expires = timezone.now() + timedelta(days=1)
        user.save()

        # Email subject and content
        subject = 'Verify your email address'
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        message = f"Please click the following link to verify your email: {verification_url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email,]

        send_mail(subject, message, from_email, recipient_list)

    @staticmethod
    def send_password_reset_email(user, token):
        """Send password reset link to the user."""

        subject = "Reset your password"
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        message = f"Please click the following link to reset your password: {reset_url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
