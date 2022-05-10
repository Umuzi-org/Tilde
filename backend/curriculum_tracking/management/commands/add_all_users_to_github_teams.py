from django.core.management.base import BaseCommand
from git_real.constants import PERSONAL_GITHUB_NAME, ORGANISATION
from social_auth.github_api import Api
from core.models import Team
from social_auth.models import SocialProfile


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("team", type=str)

    def handle(self, *args, **options):
        # team_name = options["team"]
        # team = Team.objects.get(name=team_name)
        # assert team.active, f"{team} is not active. cannot continue"
        api = Api(PERSONAL_GITHUB_NAME)

        teams = Team.objects.filter(active=True)
        total_teams = teams.count()
        # teams = [Team.objects.get(name="Boot data sci 10 Jan 2022")]
        # total_teams = 1

        api.clear_failed_organisation_invites(organisation_name=ORGANISATION)

        for i, team in enumerate(teams):
            print(f"\nprocessing team {i+1}/{total_teams}: {team.name}")
            api.create_team(organisation_name=ORGANISATION, team_name=team.name)

            users = team.user_set.filter(active=True)
            total_users = users.count()
            for j, user in enumerate(users):

                print(f"...processing user {j+1}/{total_users}: {user.email}")
                try:
                    github_name = user.social_profile.github_name
                except SocialProfile.DoesNotExist:
                    continue

                if api.user_exists(github_name=github_name):
                    api.add_user_to_team(
                        organisation_name=ORGANISATION,
                        team_name=team.name,
                        github_name=github_name,
                    )
                else:
                    print(f"github user does not exist: {github_name} {user.email}")


# TODO: add a pruning function
# if a team is not active then remove it
# what about inactive users? How do we deal with that?
