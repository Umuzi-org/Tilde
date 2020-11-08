from django.core.management.base import BaseCommand, CommandError
import datetime
from core.models import UserGroup, UserGroupMembership
from curriculum_tracking.models import RecruitProjectReview, AgileCard, ContentItem
import yaml
from ..helpers import get_student_users
from pathlib import Path
from django.utils import timezone
import logging
import csv

logger = logging.getLogger(__name__)

cutoff = timezone.now() - datetime.timedelta(days=7)
AS_REVIEWER = "AS REVIEWER"
AS_ASSIGNEE = "AS ASSIGNEE"


def sum_card_weights(cards):
    return sum([card.content_item.story_points for card in cards])


def user_as_assignee_stats(user):
    cards_with_feedback = AgileCard.objects.filter(
        status=AgileCard.REVIEW_FEEDBACK
    ).filter(assignees__in=[user])

    number_of_review_feedback_cards = cards_with_feedback.count()

    number_of_in_progress_cards = (
        AgileCard.objects.filter(status=AgileCard.IN_PROGRESS)
        .filter(assignees__in=[user])
        .count()
    )

    latest_reviews = [
        o
        for o in [
            card.recruit_project.latest_review()
            for card in cards_with_feedback
            if card.recruit_project
        ]
        if o
    ]
    latest_reviews.sort(key=lambda o: o.timestamp)

    if latest_reviews:
        oldest_review_feedback_card = latest_reviews[0].timestamp.strftime("%c")
    else:
        oldest_review_feedback_card = None

    project_cards = AgileCard.objects.filter(
        assignees__in=[user], content_item__content_type=ContentItem.PROJECT
    )
    total_number_of_project_cards = project_cards.count()
    total_weight_of_project_cards = sum_card_weights(project_cards)

    complete_projects = project_cards.filter(status=AgileCard.COMPLETE)
    number_of_complete_project_cards = complete_projects.count()
    weight_of_complete_project_cards = sum_card_weights(complete_projects)
    last_completed_project = (
        complete_projects.filter(recruit_project__complete_time__isnull=False)
        .order_by("recruit_project__complete_time")
        .last()
    )
    if last_completed_project:
        if last_completed_project.complete_time:
            last_time_a_project_was_completed = (
                last_completed_project.complete_time.strftime("%c")
            )
        else:
            last_time_a_project_was_completed = "missing data"
    else:
        last_time_a_project_was_completed = None

    return {
        "number_of_in_progress_cards": number_of_in_progress_cards,
        "number_of_review_feedback_cards": number_of_review_feedback_cards,
        "oldest_review_feedback_card": oldest_review_feedback_card,
        "number_of_complete_project_cards": number_of_complete_project_cards,
        "weight_of_complete_project_cards": weight_of_complete_project_cards,
        "total_number_of_project_cards": total_number_of_project_cards,
        "total_weight_of_project_cards": total_weight_of_project_cards,
        # "last_time_a_project_was_completed": last_time_a_project_was_completed, # TODO
    }


def recent_review_count(card, user):

    reviews = RecruitProjectReview.objects.filter(
        reviewer_user=user,
        recruit_project=card.recruit_project,
    )
    if card.review_request_time:
        reviews = reviews.filter(
            timestamp__gte=card.review_request_time,
        )

    return reviews.count()


def user_as_reviewer_stats(user):
    reviews_done_this_week = RecruitProjectReview.objects.filter(
        reviewer_user=user
    ).filter(timestamp__gte=cutoff)
    number_of_reviews_this_week = reviews_done_this_week.count()
    weight_of_reviews_this_week = sum(
        [o.recruit_project.content_item.story_points for o in reviews_done_this_week]
    )

    cards_in_review_as_reviewer = AgileCard.objects.filter(
        status=AgileCard.IN_REVIEW
    ).filter(reviewers__in=[user])

    number_of_cards_in_review_as_reviewer = cards_in_review_as_reviewer.count()
    weight_of_cards_in_review_as_reviewer = sum_card_weights(
        cards_in_review_as_reviewer
    )

    review_request_timestamps = [
        card.review_request_time
        for card in cards_in_review_as_reviewer
        if not recent_review_count(card, user)
    ]
    review_request_timestamps = [x for x in review_request_timestamps if x]
    oldest_card_awaiting_review = None
    if review_request_timestamps:
        oldest_card_awaiting_review = min(review_request_timestamps).strftime("%c")

    return {
        "number_of_reviews_done_in_last_7_days": number_of_reviews_this_week,
        "weight_of_reviews_done_in_last_7_days": weight_of_reviews_this_week,
        "number_of_cards_in_review_as_reviewer": number_of_cards_in_review_as_reviewer,
        "weight_of_cards_in_review_as_reviewer": weight_of_cards_in_review_as_reviewer,
        "oldest_card_awaiting_review": oldest_card_awaiting_review,
    }


def get_user_report(user, extra=None):
    logger.info(f"...Processing user: {user}")
    stats = {
        "_email": user.email,
        "_id": user.id,
    }

    for k, v in (extra or {}).items():
        stats[k] = v

    user_as_reviewer = user_as_reviewer_stats(user)
    user_as_assignee = user_as_assignee_stats(user)
    for s in user_as_reviewer:
        stats[f"{AS_REVIEWER} {s}"] = user_as_reviewer[s]
    for s in user_as_assignee:
        stats[f"{AS_ASSIGNEE} {s}"] = user_as_assignee[s]
    return stats


def get_group_report(group):
    logger.info(f"processing group: {group}")
    ret = [
        get_user_report(o.user, {"_group": group.name})
        for o in UserGroupMembership.objects.filter(
            group=group, user__active=True, permission_student=True
        )
    ]

    manager_users = UserGroupMembership.objects.filter(
        group=group, user__active=True, permission_manage=True
    )

    if ret == []:
        return ret

    numeric_values = {}

    for key, value in ret[0].items():
        if key.startswith("_"):
            continue
        if type(value) in [int, float]:
            numeric_values[key] = []

    for key in numeric_values:
        values = [d[key] for d in ret]

        for d in ret:
            d[f"{key} group total"] = sum(values)
            d[f"{key} group average"] = sum(values) / len(values)
            d["_group_managers"] = [o.user.email for o in manager_users]

    return ret


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.datetime.now().date()

        groups = UserGroup.objects.filter(active=True)
        all_data = []
        for group in groups:
            all_data.extend(get_group_report(group))
            # break

        headings = []
        for data in all_data:
            headings.extend(data.keys())
        headings = sorted(
            set(headings), key=lambda s: f"a{s}" if s.startswith("_") else f"b{s}"
        )

        with open(
            Path(f"gitignore/group_report_{today.strftime('%a %d %b %Y')}.csv"),
            "w",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows([[d[heading] for heading in headings] for d in all_data])
