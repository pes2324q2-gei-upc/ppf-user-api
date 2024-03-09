from django.http import HttpResponse
from ppf.common.models.user import User, Driver
from .serializers import UserSerializer
from rest_framework.response import Response

# Create your views here.


def home(request):
    users = User.objects.all()
    serializer = UserSerializer(data=users, many=True)
    return Response(serializer)
