from rest_framework.generics import ListAPIView
from common.models.achievement import UserAchievementProgress
from achievement.serializers import UserAchievementProgressSerializer


class UserAchievementList(ListAPIView):
    """
    List all achievements of a user.
    """

    serializer_class = UserAchievementProgressSerializer

    def get_queryset(self):
        user_id = self.kwargs["id"]
        return UserAchievementProgress.objects.filter(user_id=user_id)
