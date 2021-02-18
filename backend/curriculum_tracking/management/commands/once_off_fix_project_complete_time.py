"""
recruit project complet times are out of whack. This will set them to the time of the closing review
"""
from django.core.management.base import BaseCommand
from curriculum_tracking.models import (
    ContentItem,
    AgileCard,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = list(
            AgileCard.objects.filter(status=AgileCard.COMPLETE)
            .filter(content_item__content_type=ContentItem.PROJECT)
            .filter(recruit_project__complete_time__isnull=True)
        ) + list(
            AgileCard.objects.filter(status=AgileCard.COMPLETE)
            .filter(content_item__content_type=ContentItem.TOPIC)
            .filter(topic_progress__complete_time__isnull=True)
        )
        total = len(cards)
        for i, card in enumerate(cards):
            progress = card.progress_instance
            if not progress:
                continue

            print(f"{i+1}/{total}: {card}")

            review = progress.latest_review(trusted=True)
            progress.complete_time = review.timestamp
            progress.save()
