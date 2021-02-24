from social_auth.models import SocialProfile
from django.core.management.base import BaseCommand
from core.models import User
from social_auth.github_api import Api
from git_real.constants import PERSONAL_GITHUB_NAME, ORGANISATION


def list_org_outside_collaborators(api):
    page = 1
    while True:
        response = api.request(
            f"orgs/{ORGANISATION}/outside_collaborators?page={page}",
            headers={"Accept": "application/vnd.github.v3+json"},
        )
        for d in response:
            yield d["login"]
        if len(response) == 0:
            break
        page += 1


def remove_collaborator(api, github_name):
    print(f"removing {github_name}")
    response = api.delete(
        f"orgs/{ORGANISATION}/outside_collaborators/{github_name}",
        headers={"Accept": "application/vnd.github.v3+json"},
        json=False,
    )
    print(response)


class Command(BaseCommand):
    def handle(self, *args, **options):
        api = Api(PERSONAL_GITHUB_NAME)
        existing_users = list(list_org_outside_collaborators(api))
        inactive_users = User.objects.filter(active=False)
        for user in inactive_users:
            try:
                social_profile = user.social_profile
            except SocialProfile.DoesNotExist:
                continue
            if social_profile.github_name in existing_users:
                remove_collaborator(api, user.social_profile.github_name)

        active_users = User.objects.filter(active=True)
