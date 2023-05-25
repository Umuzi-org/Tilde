from django.core.management.base import BaseCommand

from git_real.constants import GIT_REAL_BOT_USERNAME, ORGANISATION

# from git_real.helpers import add_collaborator, protect_master
from curriculum_tracking.models import RecruitProject
from social_auth.github_api import Api
from long_running_request_actors import (
    recruit_project_invite_github_collaborators_to_repo,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        api = Api(GIT_REAL_BOT_USERNAME)
        for project in RecruitProject.objects.filter(
            repository__owner=ORGANISATION, recruit_users__active__in=[True]
        ):
            print(project)
            recruit_project_invite_github_collaborators_to_repo(project_id=project.id)

        # for proj in RecruitProject.objects.filter(repository__owner=ORGANISATION):
        #     repo = proj.repository
        #     print(repo)

        #     protect_master(api, repo.full_name)
        #     for user in proj.reviewer_users.all():
        #         if user.active:
        #             print(user.social_profile.github_name)
        #             add_collaborator(
        #                 api, repo.full_name, user.social_profile.github_name
        #             )
        #     for user in proj.recruit_users.all():
        #         if user.active:
        #             print(user.social_profile.github_name)
        #             add_collaborator(
        #                 api, repo.full_name, user.social_profile.github_name
        #             )
        # print()
