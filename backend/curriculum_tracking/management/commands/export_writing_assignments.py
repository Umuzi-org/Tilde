from django.core.management.base import BaseCommand
from core.models import Team
from curriculum_tracking.models import AgileCard, ContentItem
import pandas as pd

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file_name", type=str)
        parser.add_argument("team_name", type=str)
        parser.add_argument("content_item_title", type=str)

    def handle(self, *args, **options):
        team = Team.objects.get(name=options["team_name"])
        cards = AgileCard.objects.filter(content_item__content_type=ContentItem.PROJECT)
        cards_in_review = cards.filter(status=AgileCard.IN_REVIEW)
        for card in cards_in_review:
            assignee = card.assignees
            url = card.recruit_project.link_submission
