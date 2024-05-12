from rest_framework import serializers
from common.models.achievement import UserAchievementProgress


class UserAchievementProgressSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="achievement.title")
    description = serializers.CharField(source="achievement.description")
    image = serializers.ImageField(source="achievement.image")
    required_points = serializers.IntegerField(source="achievement.required_points")

    class Meta:
        model = UserAchievementProgress
        fields = [
            "title",
            "description",
            "image",
            "required_points",
            "progress",
            "date_achieved",
        ]
