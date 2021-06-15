"""
go through all repo projects. Look at the reviewers for those projects and the listed collaborators on github. Remove the extra people from the github repos
"""

from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProject
from core.models import Team
from git_real.constants import ORGANISATION, GIT_REAL_BOT_USERNAME
from git_real.helpers import list_collaborators, remove_collaborator
from social_auth.github_api import Api


class Command(BaseCommand):
    def handle(self, *args, **options):
        projects = RecruitProject.objects.filter(repository__owner=ORGANISATION)
        total = projects.count()

        api = Api(GIT_REAL_BOT_USERNAME)

        for i, project in enumerate(projects):
            print(f"project {i+1}/{total}: {project}")
            all_users = (
                list(project.recruit_users.all())
                + list(project.reviewer_users.all())
                + list(project.get_users_with_permission(Team.PERMISSION_VIEW))
            )
            expected_github_collaborators = [user.github_name for user in all_users]

            actual_collaborators = list_collaborators(
                api=api, repo_full_name=project.repository.full_name
            )

            for collaborator in actual_collaborators:
                if collaborator not in expected_github_collaborators:
                    print(f"removing: {collaborator}")
                    remove_collaborator(
                        api=api,
                        repo_full_name=project.repository.full_name,
                        github_user_name=collaborator,
                    )
