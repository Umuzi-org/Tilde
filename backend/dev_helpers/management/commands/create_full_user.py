"""Create a user and set them up for access to boards and stuff"""

from django.core.management.base import BaseCommand
from core.models import User
from social_auth.models import SocialProfile


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("is_staff", type=int)
        parser.add_argument("is_superuser", type=int)
        parser.add_argument("first_name", type=str)
        parser.add_argument("last_name", type=str)

        parser.add_argument(
            "github_name",
            type=str,
            default=None,
        )

    def handle(self, *args, **options):

        is_staff = bool(options["is_staff"])
        is_superuser = bool(options["is_superuser"])

        user, created = User.objects.get_or_create(
            email=options["email"],
            defaults={
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )
        if created:
            print("user created")
        else:
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.first_name = options["first_name"]
            user.last_name = options["last_name"]
            user.save()
            print("updated user")

        github_name = options.get("github_name")
        if github_name:
            social_profile, created = SocialProfile.objects.get_or_create(
                user=user, defaults={"github_name": github_name}
            )
            if not created:
                social_profile.github_name = github_name
                social_profile.save()