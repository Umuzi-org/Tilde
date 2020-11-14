"""
recruit project complet times are out of whack. This will set them to the time of the closing review
"""
from django.core.management.base import BaseCommand
from curriculum_tracking.models import (
    ContentItem,
    AgileCard,
    RecruitProject,
    RecruitProjectReview,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = (
            AgileCard.objects.filter(status=AgileCard.COMPLETE)
            .filter(content_item__content_type=ContentItem.PROJECT)
            .filter(recruit_project__complete_time__isnull=True)
        )
        total = cards.count()
        for i, card in enumerate(cards):
            print(f"{i+1}/{total}")
            project = card.recruit_project
            if not project:
                continue
            review = project.latest_review(trusted=True)
            project.complete_time = review.timestamp
            project.save()
