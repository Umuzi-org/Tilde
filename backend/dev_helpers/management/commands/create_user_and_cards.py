"""Create a user and set them up for access to boards and stuff"""

from django.core.management.base import BaseCommand, CommandError
from core.models import (
    User,
    Cohort,
    UserGroup,
    UserGroupMembership,
    RecruitCohort,
    Curriculum,
)

from django.utils import timezone

now = timezone.now()


def add_user_to_dev_cohort(user):
    Cohort.objects.get_or_create(
        curriculum=curriculum, defaults={"start_date": now, "end_date": now}
    )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("is_staff", type=bool)
        parser.add_argument("is_superuser", type=bool)
        parser.add_argument(
            "--github_name",
            type=str,
            default=None,
        )

    def handle(self, *args, **options):

        user, created = User.objects.get_or_create(
            email=options["email"],
            defaults={
                "is_staff": options["is_staff"],
                "is_superuser": options["is_superuser"],
            },
        )
        if not created:
            user.is_staff = options["is_staff"]
            user.is_superuser = options["is_superuser"]
            user.save()

        github_name = options.get("github_name")
        if github_name:
            social_profile, created = SocialProfile.objects.get_or_create(
                user=user, defaults={"github_name": github_name}
            )
            if not created:
                social_profile.github_name = github_name

        add_user_to_dev_cohort(user)
        # add_user_to_dev_group(user) # TODO. we'll need this when we get rid of cohorts, or when user group ui is implemtented
        add_cards_for_user(user)
