from django.core.management.base import BaseCommand, CommandError
import datetime
from core.models import UserGroup, UserGroupMembership
from curriculum_tracking.models import RecruitProjectReview, AgileCard, ContentItem
import yaml
from ..helpers import get_student_users


cutoff = datetime.datetime.now() - datetime.timedelta(days=7)


def sum_card_weights(cards):
    return sum([card.content_item.story_points for card in cards])


def user_as_assignee_stats(user):
    cards_with_feedback = AgileCard.objects.filter(
        status=AgileCard.REVIEW_FEEDBACK
    ).filter(assignees__in=[user])

    number_of_review_feedback_cards = cards_with_feedback.count()

    latest_reviews = [
        card.recruit_project.latest_review() for card in cards_with_feedback
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

    percent_projects_complete_by_weight = (
        float(weight_of_complete_project_cards) / total_weight_of_project_cards
    )
    percent_projects_complete_by_count = (
        float(number_of_complete_project_cards) / total_number_of_project_cards
    )

    return {
        "number_of_review_feedback_cards": number_of_review_feedback_cards,
        "oldest_review_feedback_card": oldest_review_feedback_card,
        "number_of_complete_project_cards": number_of_complete_project_cards,
        "weight_of_complete_project_cards": weight_of_complete_project_cards,
        "total_number_of_project_cards": total_number_of_project_cards,
        "total_weight_of_project_cards": total_weight_of_project_cards,
        # "percent_projects_complete_by_weight": percent_projects_complete_by_weight,
        # "percent_projects_complete_by_count": percent_projects_complete_by_count,
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

    return {
        "email": user.email,
        "id": user.id,
        "user_as_reviewer": user_as_reviewer_stats(user),
        "user_as_assignee": user_as_assignee_stats(user),
    }


def get_group_report(group):
    for o in UserGroupMembership.objects.filter(group=group):
        d = get_user_report(o.user)
        print(yaml.dump(d))


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("days", type=int, nargs="?", default=0)
    def handle(self, *args, **options):
        # group = UserGroup.objects.get(pk=119) #bbd
        group = UserGroup.objects.get(pk=90)  # c21 web
        d = get_group_report(group)
