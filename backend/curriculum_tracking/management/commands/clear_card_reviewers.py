from django.core.management.base import BaseCommand
from curriculum_tracking.models import ContentItem
from ..helpers import get_group, get_group_project_cards


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("group", type=str)
        parser.add_argument("content_item", type=str)

    def handle(self, *args, **options):

        group_name = options["group"]
        group = get_group(group_name)

        content_item_name = options["content_item"]
        content_item = ContentItem.objects.get(
            title=content_item_name, content_type=ContentItem.PROJECT
        )

        cards = get_group_project_cards(group, content_item)

        for card in cards:
            card.reviewers.set([])
            if card.recruit_project:
                card.recruit_project.reviewer_users.set([])