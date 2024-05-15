"""
How long are learners waiting for reviews?

"E5 - core: web dev"
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from curriculum_tracking.models import RecruitProjectReview, AgileCard, ContentItem
from activity_log.models import LogEntry
from curriculum_tracking.activity_log_entry_creators import CARD_REVIEW_REQUESTED
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("who")

    def handle(self, *args, **options):
        who = options["who"]
        users = User.get_users_from_identifier(who)

        complete_cards = (
            AgileCard.objects.filter(assignees__in=users)
            .filter(content_item__content_type=ContentItem.PROJECT)
            .filter(status=AgileCard.COMPLETE)
            .prefetch_related("recruit_project")
        )

        for card in complete_cards:
            project = card.recruit_project

        timeline = []

        log_entries = LogEntry.objects.filter(
            object_1_content_type=ContentType.objects.get_for_model(project),
            object_1_id=project.id,
        ).prefetch_related("event_type")

        for entry in log_entries:
            timeline.append(
                {
                    "timestamp": entry.timestamp,
                    "event_type": entry.event_type.name,
                    "actor": entry.actor_user.email,
                }
            )

        reviews = RecruitProjectReview.objects.filter(recruit_project=project)

        for review in reviews:
            timeline.append(
                {
                    "timestamp": review.timestamp,
                    "event_type": f"REVIEW {review.status_nice} validated={review.validated_nice} trusted={review.trusted}",
                    "actor": review.reviewer_user.email,
                }
            )

        timeline.sort(key=lambda x: x["timestamp"])
