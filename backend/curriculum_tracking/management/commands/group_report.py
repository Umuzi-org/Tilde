from django.core.management.base import BaseCommand, CommandError
import datetime
from core.models import UserGroup, UserGroupMembership
from curriculum_tracking.models import RecruitProjectReview, AgileCard, ContentItem
import yaml
from ..helpers import get_student_users
from pathlib import Path
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

cutoff = timezone.now() - datetime.timedelta(days=7)


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
        card.recruit_project.latest_review()
        for card in cards_with_feedback
        if card.recruit_project
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
        "last_time_a_project_was_completed": last_time_a_project_was_completed,
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


def get_user_report(user):
    logger.info(f"...Processing user: {user}")
    return {
        "email": user.email,
        "id": user.id,
        "user_as_reviewer": user_as_reviewer_stats(user),
        "user_as_assignee": user_as_assignee_stats(user),
    }


def get_group_report(group):
    logger.info(f"processing group: {group}")
    return {
        o.user.email: get_user_report(o.user)
        for o in UserGroupMembership.objects.filter(group=group, user__active=True)
    }


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.datetime.now().date()

        groups = UserGroup.objects.filter(active=True)
        for group in groups:
            group_data = get_group_report(group)

            with open(
                Path(f"gitignore/group_report_{today.strftime('%a %d %b %Y')}.yaml"),
                "w",
            ) as f:
                yaml.dump(group_data, f)
