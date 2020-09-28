from django.core.management.base import BaseCommand, CommandError

from core import models as core_models
from git_real.constants import (
    ORGANISATION,
    GITHUB_DATETIME_FORMAT,
    PERSONAL_GITHUB_NAME,
)
from git_real import models
from git_real import helpers
from social_auth.github_api import Api
from social_auth import models as social_models


def scrape_and_save_organisation_repos(api, organisation_name):
    repo_dicts = api.request_pages(f"orgs/{organisation_name}/repos")
    for repo in repo_dicts:
        helpers.save_repo(repo)  # (#161)


def scrape_and_save_user_repos(api, username, user):
    print(f"\nfetching repos for: {user}")
    repo_dicts = api.request_pages(f"users/{username}/repos", response404=[])
    for repo in repo_dicts:
        helpers.save_repo(repo, user)


def scrape_repos_from_github():
    api = Api(PERSONAL_GITHUB_NAME)

    scrape_and_save_organisation_repos(api, ORGANISATION)

    for user in core_models.User.objects.filter(active=True,):
        try:
            profile = social_models.SocialProfile.objects.get(user=user)
        except social_models.SocialProfile.DoesNotExist:
            continue
        if profile.github_name:
            github_name = profile.github_name
            scrape_and_save_user_repos(api, github_name, user)


class Command(BaseCommand):
    def handle(self, *args, **options):
        scrape_repos_from_github()
