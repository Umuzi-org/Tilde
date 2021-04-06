from django.core.management.base import BaseCommand
from git_real.constants import PERSONAL_GITHUB_NAME, ORGANISATION
from social_auth.github_api import Api
from core.models import Team
from social_auth.models import SocialProfile


def create_github_team(team_name, api):
    api.post(
        f"orgs/{ORGANISATION}/teams",
        data={"description": "Automatically generated team", "name": team_name},
        headers={"accept": "application/vnd.github.v3+json"},
    )


def add_user_to_team(team_name, user, api):
    try:
        github_name = user.social_profile.github_name
    except SocialProfile.DoesNotExist:
        return

    api.put(
        f"orgs/{ORGANISATION}/memberships/{github_name}",
        headers={"accept": "application/vnd.github.v3+json"},
        data={},
    )

    api.put(
        f"orgs/{ORGANISATION}/teams/{team_name}/memberships/{github_name}",
        headers={"accept": "application/vnd.github.v3+json"},
        data={},
    )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("team", type=str)

    def handle(self, *args, **options):
        team_name = options["team"]
        team = Team.objects.get(name=team_name)
        assert team.active, f"{team} is not active. cannot continue"
        api = Api(PERSONAL_GITHUB_NAME)

        create_github_team(team_name, api)
        for user in team.user_set.filter(active=True):
            add_user_to_team(team_name, user, api)
