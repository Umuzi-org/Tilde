"""Create a user and set them up for access to boards and stuff"""

from django.core.management.base import BaseCommand
from core.models import User
from social_auth.models import SocialProfile


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("is_staff", type=bool)
        parser.add_argument("is_superuser", type=bool)
        parser.add_argument(
            "github_name",
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
                social_profile.save()