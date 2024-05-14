from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from common.models.achievement import UserAchievementProgress
from common.models.route import Route


# Create 1, 10 and 50 routes
@receiver(m2m_changed, sender=Route.passengers.through)
def route_created(sender, instance, created, **kwargs):
    nRoutesDriver = Route.objects.filter(driver=instance.driver).count()
    # nRoutesDriver == 1
    if created:
        try:
            UserAchievementProgress.objects.get_or_create(
                user=instance.driver,
                achievement_id=1,
                progress=1,
                achieved=True,
                date_achieved=instance.created_at,
            )
        except Exception as e:
            print(e)
            pass
