"""
    This module contains the view used to send an email to the site owner.
"""

from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render

from .serializers import PasswordResetRequestSerializer, SetNewPasswordSerializer
from common.models.user import User


def reset_password_page(request):
    return render(request, "reset_pass_page.html")


class PasswordResetRequestView(GenericAPIView):
    """
    This view sends the email with the link to reset the password
    """

    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            # Temporal token to authenticate the user for password reset
            token = default_token_generator.make_token(user)
            # User ID byte encoded in base64 to pass it in the URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"http://localhost:8081/reset-password-page/?uid={uid}&token={token}"

            subject = "Password Reset Requested"
            message = f"""
            Hi {user.username},

            You requested a password reset. Click the link below to reset your password:

            {reset_url}

            If you did not make this request, you can ignore this email.

            Thanks,
            PowerPathFinder Team
            """
            from_email = settings.EMAIL_HOST_USER

            send_mail(subject, message, from_email, [email], fail_silently=False)

            return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(GenericAPIView):
    """
    This views check if the token is valid and sets the new password
    """

    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data["uidb64"]
            new_password = serializer.validated_data["new_password"]

            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()

            # Invalidate all auth tokens for the user
            Token.objects.filter(user=user).delete()

            return Response(
                {"message": "Password has been reset successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
