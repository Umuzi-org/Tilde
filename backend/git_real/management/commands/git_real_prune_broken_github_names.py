""" if there is a typo in a recruit's github name, then remove the name and log the error"""
from django.core.management.base import BaseCommand, CommandError

from social_auth import models as social_models
from social_auth.github_api import Api
from git_real.constants import PERSONAL_GITHUB_NAME


# GET /users/:username


def check_git_usernames():
    api = Api(PERSONAL_GITHUB_NAME)
    for social_profile in social_models.SocialProfile.objects.all():
        if social_profile.github_name:
            social_profile.github_name = social_profile.github_name.strip()
            NOT_FOUND = "notfound"
            response = api.request(
                f"users/{social_profile.github_name}", response404=NOT_FOUND
            )
            if response == NOT_FOUND:
                print(f"{social_profile.user.email}: {social_profile.github_name}")
                social_profile.github_name = None
            social_profile.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_git_usernames()
