Deprecated

"""Doesn't look like anything is using this"""

from django.core.management.base import BaseCommand
from core.models import Team
from curriculum_tracking.models import RecruitProject, ContentItem
import csv


def get_user_and_projectlink(team, content_item):
    results = []
    for user in team.active_users:
        project = RecruitProject.objects.filter(
            recruit_users__in=[user], content_item=content_item
        ).first()
        results.append(
            [user.email, project and (project.link_submission or project.git_url)]
        )
    return results


class Command(BaseCommand):
    """python manage.py export_project_urls <team> <project>"""

    def add_arguments(self, parser):
        parser.add_argument("team_name", type=str)
        parser.add_argument("content_item_title", type=str)

    def handle(self, *args, **options):
        team = Team.objects.get(name=options["team_name"])
        content_item = ContentItem.objects.get(title=options["content_item_title"])
        results = get_user_and_projectlink(team, content_item)

        with open(f"gitignore/{team}_{content_item}_urls.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["user_email", "url"])
            writer.writerows(results)
