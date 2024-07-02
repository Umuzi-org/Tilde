"""
get a list of projects that were recently started that we have not many trusted people for
"""

from django.core.management.base import BaseCommand
from curriculum_tracking.models import RecruitProject, ReviewTrust
import csv
from django.utils import timezone
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = timezone.now() - timezone.timedelta(days=14)
        projects = RecruitProject.objects.filter(
            Q(start_time__gte=cutoff) | Q(review_request_time__gte=cutoff)
        ).prefetch_related("content_item")

        trusted_per_project = {}

        for project in projects:
            title = project.content_item.title
            flavours = project.flavour_names

            identifier = f"{title} {flavours}"
            if identifier in trusted_per_project:
                continue

            trusts = ReviewTrust.objects.filter(content_item=project.content_item)

            trusted_per_project[identifier] = [
                o.user.email for o in trusts if o.flavours_match(flavours)
            ]

        with open("gitignore/recent_projects_and_trusted_reviewers.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["project", "trusted"])

            for key, emails in sorted(
                trusted_per_project.items(), key=lambda t: len(t[1])
            ):
                writer.writerow([key, ", ".join(emails)])
