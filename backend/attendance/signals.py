from attendance.models import MorningAttendance, AfternoonAttendance, EveningAttendance
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.db.models import Sum

from django.core.exceptions import ObjectDoesNotExist


@receiver([post_save], sender=MorningAttendance)
@receiver([post_save], sender=AfternoonAttendance)
@receiver([post_save], sender=EveningAttendance)
def update_denorm(sender, instance, **kwargs):
    if instance.is_staff in [True, False]:
        return
    instance.is_staff = instance.user.is_staff
    try:
        instance.cohort = (
            instance.user.recruit_cohorts and instance.user.recruit_cohorts.cohort
        )
    except ObjectDoesNotExist:
        instance.cohort = None

    instance.product_teams.set(instance.user.product_teams.all())

    instance.save()
