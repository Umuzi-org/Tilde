"""
python manage.py setup_recent_project_repos 1
"""

from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProject, ContentItem
from django.utils import timezone


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "days_since",
            type=int,
        )

    def handle(self, *args, **options):
        days_since = options["days_since"]

        start = timezone.now() - timezone.timedelta(days=days_since)

        projects = RecruitProject.objects.filter(start_time__gte=start).filter(
            content_item__project_submission_type=ContentItem.REPOSITORY
        )
        total = projects.count()
        for i, project in enumerate(projects):
            print(f"setting up project {i+1}/{total}: {project}")
            project.setup_repository()
