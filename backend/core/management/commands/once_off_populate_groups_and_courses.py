from django.core.management.base import BaseCommand, CommandError
from core.models import ProductTeam, Cohort, UserGroup, UserGroupMembership
from curriculum_tracking.models import CourseRegistration
from django.contrib.auth import get_user_model

User = get_user_model()


def process_product_teams():
    for team in ProductTeam.objects.all():
        group, _ = UserGroup.objects.get_or_create(
            name=team.name, kind=UserGroup.PRODUCT_TEAM
        )
        for user in team.users.all():
            UserGroupMembership.objects.get_or_create(user=user, group=group)


def process_cohorts():
    for cohort in Cohort.objects.all():
        attributes = {"active": cohort.active}
        group, _ = UserGroup.get_or_create_or_update(
            name=cohort.__str__(),
            kind=UserGroup.COHORT,
            overrides=attributes,
            defaults=attributes,
        )
        for cohort_user in cohort.cohort_recruits.all():
            UserGroupMembership.objects.get_or_create(
                user=cohort_user.user, group=group
            )
            CourseRegistration.objects.get_or_create(
                user=cohort_user.user, curriculum=cohort.cohort_curriculum
            )


class Command(BaseCommand):
    def handle(self, *args, **options):
        process_cohorts()
        process_product_teams()
