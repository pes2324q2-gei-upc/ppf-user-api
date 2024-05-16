from django.db.models.signals import post_save
from django.dispatch import receiver
from common.models.achievement import UserAchievementProgress, Achievement
from common.models.valuation import Valuation
from common.models.user import User


"""
# Only if we need to created with antecipation all the achievements for a user
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        for achievement in Achievement.objects.all():
            UserAchievementProgress.objects.create(user=instance, achievement=achievement)"""


# Valuate 1 user
@receiver(post_save, sender=Valuation)
def user_valuated(sender, instance, created, **kwargs):
    if created:
        try:
            achievement = Achievement.objects.get(title="CriticoEstelar")
        except Achievement.DoesNotExist:
            return

        user_achievement, _ = UserAchievementProgress.objects.get_or_create(
            user=instance.giver, achievement=achievement
        )

        check_and_increment_progress(user_achievement, achievement, instance)


# Change 1 time the user profile
# Driver is a subclass of User, when a driver is updated, the user is updated too
# so the signal will be triggered.
@receiver(post_save, sender=User)
def user_changed_profile(sender, instance, created, **kwargs):
    if not (created):
        try:
            achievement = Achievement.objects.get(title="Camaleon")
        except Achievement.DoesNotExist:
            return

        user_achievement, _ = UserAchievementProgress.objects.get_or_create(
            user=instance, achievement=achievement
        )

        check_and_increment_progress(user_achievement, achievement, instance)


def check_and_increment_progress(user_achievement, achievement, instance):
    if not user_achievement.achieved:
        user_achievement.progress += 1
        if user_achievement.progress >= achievement.required_points:
            user_achievement.achieved = True
            user_achievement.date_achieved = instance.createdAt
        user_achievement.save()
