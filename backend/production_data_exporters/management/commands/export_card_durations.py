"""
How long are learners waiting for reviews?

"E5 - core: web dev"
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from curriculum_tracking.models import RecruitProjectReview, AgileCard, ContentItem
from activity_log.models import LogEntry
from django.contrib.contenttypes.models import ContentType
import csv
from curriculum_tracking.activity_log_entry_creators import (
    CARD_REVIEW_REQUESTED,
    CARD_MOVED_TO_REVIEW_FEEDBACK,
)
from datetime import timedelta

User = get_user_model()


def first_review_request_time(project):
    return (
        LogEntry.objects.filter(
            event_type__name=CARD_REVIEW_REQUESTED,
            object_1_content_type=ContentType.objects.get_for_model(project),
            object_1_id=project.id,
        )
        .order_by("timestamp")
        .first()
        .timestamp
    )


def get_number_of_review_requests(project):
    return LogEntry.objects.filter(
        event_type__name=CARD_REVIEW_REQUESTED,
        object_1_content_type=ContentType.objects.get_for_model(project),
        object_1_id=project.id,
    ).count()


def ave_delay_between_feedback_and_review_request(project):
    feedback_given_logs = LogEntry.objects.filter(
        event_type__name=CARD_MOVED_TO_REVIEW_FEEDBACK,
        object_1_content_type=ContentType.objects.get_for_model(project),
        object_1_id=project.id,
    )

    cycles = 0
    total_duration = timedelta(0)

    for entry in feedback_given_logs:
        feedback_timestamp = entry.timestamp
        review_request = LogEntry.objects.filter(
            event_type__name=CARD_REVIEW_REQUESTED,
            object_1_content_type=ContentType.objects.get_for_model(project),
            object_1_id=project.id,
            timestamp__gte=feedback_timestamp,  # only consider review requests after feedback
        ).first()
        if review_request:
            cycles += 1
            total_duration += review_request.timestamp - feedback_timestamp

    if cycles:
        return total_duration / cycles


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
            .prefetch_related("content_item")
            .prefetch_related("recruit_project")
        )

        l = [
            {
                "assignee": card.assignee_names[0],
                "title": card.content_item.title,
                "start_time": card.recruit_project.start_time,
                "first_review_request_time": first_review_request_time(
                    card.recruit_project
                ),
                "complete_time": card.recruit_project.complete_time,
                "duration": card.recruit_project.complete_time
                - card.recruit_project.start_time,
                "number_of_review_requests": get_number_of_review_requests(
                    card.recruit_project
                ),
                "ave_delay_between_feedback_and_review_request": ave_delay_between_feedback_and_review_request(
                    card.recruit_project
                ),
                "link": f"https://backend.tilde.umuzi.org/progress_details/project/{card.recruit_project.id}",
            }
            for card in complete_cards
        ]

        for d in l:
            d["time_from_first_review_request_to_close"] = (
                d["complete_time"] - d["first_review_request_time"]
            )
        l.sort(key=lambda x: -x["time_from_first_review_request_to_close"])

        with open(f"gitignore/project_durations_{who}.csv", "w") as f:
            writer = csv.writer(f)
            headers = list(l[0].keys())
            writer.writerow(headers)

            for d in l:
                writer.writerow([d[s] for s in headers])


#         projects = {}

#         for card in complete_cards:
#             project = card.recruit_project

#             timeline = []

#             log_entries = LogEntry.objects.filter(
#                 object_1_content_type=ContentType.objects.get_for_model(project),
#                 object_1_id=project.id,
#             ).prefetch_related("event_type")

#             for entry in log_entries:
#                 timeline.append(
#                     {
#                         "timestamp": entry.timestamp,
#                         "event_type": entry.event_type.name,
#                         "actor": entry.actor_user.email,
#                     }
#                 )

#             reviews = RecruitProjectReview.objects.filter(recruit_project=project)

#             for review in reviews:
#                 timeline.append(
#                     {
#                         "timestamp": review.timestamp,
#                         "event_type": f"REVIEW {review.status_nice} validated={review.validated_nice} trusted={review.trusted}",
#                         "actor": review.reviewer_user.email,
#                     }
#                 )

#             timeline.sort(key=lambda x: x["timestamp"])

#             projects[project.id] = timeline

#         breakpoint()

#         wee
