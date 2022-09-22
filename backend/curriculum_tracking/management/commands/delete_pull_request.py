from django.core.management.base import BaseCommand

from curriculum_tracking.models import AgileCard
from git_real.models import PullRequest


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("card_id", type=int)
        parser.add_argument("pr_number", type=int)

    def handle(self, *args, **options):
        card = AgileCard.objects.get(pk=options["card_id"])
        prs = PullRequest.objects.filter(number=options["pr_number"]).filter(
            repository__recruit_projects__agile_card=card
        )

        assert len(prs) == 1, len(prs)

        prs.delete()
