from django.core.management.base import BaseCommand
from curriculum_tracking.models import FlavourMixin, AgileCard, Team
from datetime import datetime
from ..helpers import get_users


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("team", type=str)
        parser.add_argument("content_item_id", type=int)
        parser.add_argument("flavour", type=str)

    def handle(self, *args, **options):
        team = team = Team.objects.get(name=options["team"])
        content_item_id = options["content_item_id"]
        flavours = [flavour for flavour in options["flavour"].split(",") if flavour]

        time = datetime.now()

        for member in team.active_users:
            breakpoint()
            AgileCard.set_due_time(member, time)