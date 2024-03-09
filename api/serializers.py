from rest_framework import serializers
from ppf.common.models.user import MyUser, Driver


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"
