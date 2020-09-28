from django.core.management.base import BaseCommand

from git_real.constants import PERSONAL_GITHUB_NAME

from git_real.helpers import create_repo_and_assign_contributer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("repo_full_name", type=str)
        parser.add_argument("github_user_name", type=str)
        parser.add_argument("readme_text", type=str)

    def handle(self, *args, **options):
        create_repo_and_assign_contributer(
            github_auth_login=PERSONAL_GITHUB_NAME,
            repo_full_name=options["repo_full_name"],
            github_user_name=options["github_user_name"],
            readme_text=options["readme_text"],
        )


"""
python manage.py git_real_create_single_repo "Umuzi-org/ttestingtestingtestingtestingtestingtestingtestingtestingtestgtestingtestingtestingtestingtesting124" "sheenarbw" "just testing repo creation. Feel free to totally ignore this"
"""
