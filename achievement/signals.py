from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from common.models.achievement import UserAchievementProgress, Achievement
from common.models.valuation import Valuation
from common.models.user import User, Driver


def initialize_achievements(user):
    achievements = Achievement.objects.all()
    for achievement in achievements:
        # Check if the user already has the achievement
        if not UserAchievementProgress.objects.filter(user=user, achievement=achievement).exists():
            UserAchievementProgress.objects.create(user=user, achievement=achievement)


# Inicialize all the achievements for the user
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        initialize_achievements(instance)


# Inicialize all the achievements for the driver
@receiver(post_save, sender=Driver)
def driver_created(sender, instance, created, **kwargs):
    if created:
        initialize_achievements(instance)


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


@receiver(pre_save, sender=User)
def cache_old_profile_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_profile_image = User.objects.get(pk=instance.pk).profileImage
        except User.DoesNotExist:
            instance._old_profile_image = None
    else:
        instance._old_profile_image = None


# Change 1 time the user profile
# Driver is a subclass of User, when a driver is updated, the user is updated too
# so the signal will be triggered.
@receiver(post_save, sender=User)
def user_changed_profile(sender, instance, created, **kwargs):
    if not created:
        old_profile_image = getattr(instance, "_old_profile_image", None)
        new_profile_image = instance.profileImage

        if old_profile_image != new_profile_image:

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
