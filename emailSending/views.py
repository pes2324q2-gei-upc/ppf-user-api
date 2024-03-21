"""
    This module contains the view used to send an email to the site owner.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from .serializers import EmailSerializer


class SendEmailView(APIView):
    """
    The class that send an email.

    Args:
        APIView: Base class for handling HTTP requests.
    """

    @swagger_auto_schema(
        request_body=EmailSerializer,
        responses={
            200: "Email sent successfully",
            400: "Bad request",
        },
    )
    def post(self, request):
        """
            Handle POST request for sending an email.

            Parameters:
            - request: HTTP request object containing an email.

            Returns:
            - Response: HTTP response object containing a information message
            if successful, or an error message if there is any error.
        """

        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            inquiry = serializer.validated_data.get('inquiry')
            message = serializer.validated_data.get('message')

            send_mail(
                subject=inquiry,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.RECIPIENT_ADDRESS]
            )

            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
