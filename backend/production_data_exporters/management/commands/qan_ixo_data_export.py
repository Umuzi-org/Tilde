"""
Coderbyte test data: https://airtable.com/appkr1uRo6nZXyeZb/tblOUhSvLGQha8AAI/viw1R15ro6ExI8ySp?blocks=hide 
"""


from django.core.management.base import BaseCommand

from core.models import Team, Stream
from curriculum_tracking.models import AgileCard, ContentItem
from pathlib import Path
from django.utils import timezone
import csv

team_names = ["Cohort C40I web dev", "C42i - core: web dev"]
stream_name = "core: web dev"


training_provider_id = 1
training_provider_name = "Umuzi"


def save_summary(stream_id, today, now, users):
    file_path = Path(f"gitignore/isa_card_summary_export_{today}.csv")

    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "timestamp",
                "user_id",
                "user_email",
                "cohort_id",
                "cohort_name",
                "total_project_cards",
                "total_project_core_cards",
                "total_project_core_cards_completed",
                "total_project_cards_completed",
                "course_id",
                "course_name",
            ]
        )

        for user, team in users:
            cards = AgileCard.objects.filter(assignees=user).filter(
                content_item__content_type=ContentItem.PROJECT
            )
            complete_cards = cards.filter(recruit_project__complete_time__isnull=False)
            core_cards = cards.filter(is_hard_milestone=True)
            core_complete_cards = complete_cards.filter(is_hard_milestone=True)

            row = [
                now,
                user.id,
                user.email,
                team.id,
                team.name,
                cards.count(),
                core_cards.count(),
                core_complete_cards.count(),
                complete_cards.count(),
                stream_id,
                stream_name,
            ]

            writer.writerow(row)


class Command(BaseCommand):
    def handle(self, *args, **options):
        teams = [Team.objects.get(name=name) for name in team_names]
        users = [(user, team) for team in teams for user in team.user_set.all()]

        now = timezone.now()
        today = now.strftime("%Y-%m-%d")

        stream_id = Stream.objects.get(name=stream_name).id

        # save_summary(stream_id=stream_id, users=users, today=today, now=now)

        file_path = Path(f"gitignore/isa_completed_cards_export_{today}.csv")

        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "timestamp",
                    "user_id",
                    "content_item_id",
                    "content_item_title",
                    "closing_review_timestamp",
                    "closing_review_comments",
                    "closing_review_reviewer_email",
                    "closing_review_reviewer_id",
                    "course_id",
                    "course_name",
                    "training_provider_id",
                    "training_provider_name",
                ]
            )

            cards = (
                AgileCard.objects.filter(assignees__in=[u[0] for u in users])
                .filter(content_item__content_type=ContentItem.PROJECT)
                .filter(recruit_project__complete_time__isnull=False)
                .prefetch_related("recruit_project__project_reviews")
                .prefetch_related("content_item")
                .prefetch_related("assignees")
            )

            for card in cards:
                closing_review = card.recruit_project.project_reviews.order_by(
                    "timestamp"
                ).last()
                row = [
                    now,
                    card.assignees.first().id,
                    card.content_item.id,
                    card.content_item.title,
                    closing_review.timestamp,
                    closing_review.comments,
                    closing_review.reviewer_user.email,
                    closing_review.reviewer_user.id,
                    stream_id,
                    stream_name,
                    training_provider_id,
                    training_provider_name,
                ]
                writer.writerow(row)
