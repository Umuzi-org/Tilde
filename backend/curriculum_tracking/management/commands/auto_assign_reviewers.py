from curriculum_tracking.management.auto_assign_reviewers import auto_assign_reviewers
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("skip_teams", type=str, nargs="*")

    def handle(self, *args, **options):
        auto_assign_reviewers()
