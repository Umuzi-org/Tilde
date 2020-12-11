from django.core.management.base import BaseCommand, CommandError
from core.models import ProductTeam, Cohort, Team, TeamMembership
from curriculum_tracking.models import CourseRegistration
from django.contrib.auth import get_user_model

User = get_user_model()


def process_product_teams():
    for team in ProductTeam.objects.all():
        group, _ = Team.objects.get_or_create(name=team.name, kind=Team.PRODUCT_TEAM)
        for user in team.users.all():
            TeamMembership.objects.get_or_create(user=user, group=group)


def process_cohorts():
    for cohort in Cohort.objects.all():
        attributes = {"active": cohort.active}
        group, _ = Team.get_or_create_or_update(
            name=cohort.__str__(),
            kind=Team.COHORT,
            overrides=attributes,
            defaults=attributes,
        )
        for cohort_user in cohort.cohort_recruits.all():
            TeamMembership.objects.get_or_create(user=cohort_user.user, group=group)
            CourseRegistration.objects.get_or_create(
                user=cohort_user.user, curriculum=cohort.cohort_curriculum
            )


class Command(BaseCommand):
    def handle(self, *args, **options):
        process_cohorts()
        process_product_teams()
