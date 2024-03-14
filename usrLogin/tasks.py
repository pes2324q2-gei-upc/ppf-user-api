from django.utils import timezone
from rest_framework.authtoken.models import Token


def limpiar_tokens_expirados():
    tokens_expirados = Token.objects.filter(expires__lt=timezone.now())
    tokens_expirados.delete()
