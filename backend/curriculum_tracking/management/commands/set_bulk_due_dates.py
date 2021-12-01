from django.core.management.base import BaseCommand
from curriculum_tracking.models import AgileCard, Team
from ..helpers import get_team_cards


class Command(BaseCommand):
    """
    Generic command structure: python manage.py set_bulk_due_dates "team_name" "content_item_id" "flavour" "YYYY-MM-DD"
    command example: python manage.py set_bulk_due_dates bomb_squad 2 Python 2021-02-18
    """

    def add_arguments(self, parser):
        parser.add_argument("team", type=str)
        parser.add_argument("content_item_id", type=int)
        parser.add_argument("flavour", type=str)
        parser.add_argument("date", type=str)

    def handle(self, *args, **options):
        team = Team.objects.get(name=options["team"])
        content_item_id = options["content_item_id"]
        due_date = options["date"]
        flavours = [flavour for flavour in options["flavour"].split(",") if flavour]
        team_cards = get_team_cards(team, content_item_id)

        for card in team_cards:
            if card.flavours_match(flavours):
                AgileCard.set_due_time(card, due_date)