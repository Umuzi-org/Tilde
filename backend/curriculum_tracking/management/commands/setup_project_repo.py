"""
python manage.py setup_project_repo "Tilde project tutorial: How Repo projects work" "sheena.oconnell@gmail.com" ""
"""

from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProject


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("content_item", type=str)
        parser.add_argument("assignee", type=str)
        parser.add_argument("flavours", type=str)

    def handle(self, *args, **options):
        assignee = options["assignee"]
        content_item = options["content_item"]
        flavours = [s for s in options["flavours"].split(",") if s]
        projects = RecruitProject.objects.filter(recruit_users__email__in=[assignee])
        projects = projects.filter(content_item__title=content_item)

        found = False
        for project in projects:
            if project.flavours_match(flavours):
                print("found a match")
                found = True
                project.setup_repository()

        assert found, "no matching project found!"
