"""Get some recent projects that match the given criteria. Print out their repo urls and card urls.

Usage:
    python manage.py recent_projects <content_item_id> <flavours> <is_complete> <limit
    if is_complete is False then look for projects in the review column 
"""
from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProject, AgileCard


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("content_item_id", type=int)
        parser.add_argument("flavours", type=str)
        parser.add_argument("is_complete", type=bool)
        parser.add_argument("limit", type=int, nargs="?", default=10)

    def handle(self, *args, **options):
        content_item_id = options["content_item_id"]
        flavours = options["flavours"].split(",")
        is_complete = options["is_complete"]
        limit = options["limit"]

        projects = RecruitProject.objects.filter(content_item__id=content_item_id)
        if is_complete:
            projects = projects.filter(complete_time__isnull=False).order_by(
                "-complete_time"
            )
        else:
            projects = (
                projects.filter(complete_time__isnull=True)
                .filter(review_request_time__isnull=True)
                .order_by("-review_request_time")
            )

        total = 0
        for project in projects:
            if project.flavours_match(flavours):
                try:
                    card_id = project.agile_card.id
                except AgileCard.DoesNotExist:
                    continue
                card_url = f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card_id}"
                repo_name = project.repository.full_name
                github_url = f"https://github.com/{repo_name}"
                clone_url = project.repository.ssh_url

                print(f"{card_url}\n{github_url}\n{clone_url}\n\n")
                total += 1
                if total >= limit:
                    break
