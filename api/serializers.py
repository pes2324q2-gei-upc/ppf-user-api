from rest_framework import serializers
from ppf.common.models.user import User, Driver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
