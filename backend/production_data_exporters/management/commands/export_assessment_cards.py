from django.core.management.base import BaseCommand
from curriculum_tracking.models import AgileCard
import csv
from django.utils import timezone
from curriculum_tracking.constants import COMPETENT, EXCELLENT


def list_positive_reviewers(card):
    if card.recruit_project:
        queryset = card.recruit_project.project_reviews.all()
        if card.review_request_time:
            queryset = queryset.filter(timestamp__gt=card.review_request_time)
        return ", ".join(
            [
                r.reviewer_user.email
                for r in queryset
                if r.status in [COMPETENT, EXCELLENT]
            ]
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        cards = AgileCard.objects.filter(
            content_item__title__startswith="Assessment:"
        ).filter(assignees__active__in=[True])
        today = timezone.now().date()

        with open(
            f"gitignore/assessment_cards_{today.strftime('%a %d %b %Y')}.csv", "w"
        ) as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "assignee",
                    "title",
                    "status",
                    "card_id",
                    "flavours",
                    "positive_reviewers",
                ]
            )
            for card in cards:
                writer.writerow(
                    [
                        ", ".join([a.email for a in card.assignees.all()]),
                        card.title,
                        card.status,
                        card.id,
                        ", ".join(card.flavour_names),
                        list_positive_reviewers(card),
                        # card.recruit_project.code_review_competent_since_last_review_request,
                    ]
                )
