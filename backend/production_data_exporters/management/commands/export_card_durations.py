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
from git_real.activity_log_creators import PR_OPENED, PR_CLOSED, PR_MERGED
from datetime import timedelta
from django.db.models import Q

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


def total_prs_reviewed(project):
    if project.repository is None:
        return 0
    return project.repository.pull_requests.filter(
        Q(closed_at__isnull=True) | Q(merged_at__isnull=True)
    ).count()


def total_pr_review_wait_time(project):
    """time that the learner was waiting for a review or close"""
    if project.repository is None:
        return timedelta(0)
    pull_requests = project.repository.pull_requests.filter(
        Q(closed_at__isnull=True) | Q(merged_at__isnull=True)
    )
    wait_time = timedelta(0)
    count = len(pull_requests)
    for pr in pull_requests:

        if pr.closed_at:
            wait_time += pr.closed_at - pr.created_at
        if pr.merged_at:
            wait_time += pr.merged_at - pr.created_at
    return wait_time


def sum_delay_between_feedback_and_review_request(project):
    feedback_given_logs = LogEntry.objects.filter(
        event_type__name=CARD_MOVED_TO_REVIEW_FEEDBACK,
        object_1_content_type=ContentType.objects.get_for_model(project),
        object_1_id=project.id,
    )

    total_duration = timedelta(0)

    seen = set()
    for entry in feedback_given_logs:
        feedback_timestamp = entry.timestamp
        review_request = LogEntry.objects.filter(
            event_type__name=CARD_REVIEW_REQUESTED,
            object_1_content_type=ContentType.objects.get_for_model(project),
            object_1_id=project.id,
            timestamp__gte=feedback_timestamp,  # only consider review requests after feedback
        ).first()
        if review_request:
            if review_request.id in seen:
                continue
            seen.add(review_request.id)
            total_duration += review_request.timestamp - feedback_timestamp
    return total_duration


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
                "total_pr_review_wait_time": total_pr_review_wait_time(
                    card.recruit_project
                ),
                "total_prs_reviewed": total_prs_reviewed(card.recruit_project),
                "complete_time": card.recruit_project.complete_time,
                "duration": card.recruit_project.complete_time
                - card.recruit_project.start_time,
                "number_of_review_requests": get_number_of_review_requests(
                    card.recruit_project
                ),
                "sum_delay_between_feedback_and_review_request": sum_delay_between_feedback_and_review_request(
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
