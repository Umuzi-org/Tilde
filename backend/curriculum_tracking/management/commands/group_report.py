from django.core.management.base import BaseCommand
import datetime
from core.models import Team
from curriculum_tracking.models import RecruitProjectReview, AgileCard, ContentItem
from pathlib import Path
from django.utils import timezone
import logging
import csv
from curriculum_tracking.constants import (
    COMPETENT,
    EXCELLENT,
)
from django.db.models import Q


logger = logging.getLogger(__name__)

AS_REVIEWER = "R"
AS_ASSIGNEE = "A"


DATE_FORMAT = "%-d-%b-%y"
# dd-mmm-yy
# eg. 12-Nov-20


accumulated_user_as_reviewer_stats = {}
accumulated_user_as_assignee_stats = {}


def sum_card_weights(cards):
    return sum([card.content_item.story_points for card in cards])


def user_as_assignee_stats(user):
    cards_in_review_column = AgileCard.objects.filter(
        status=AgileCard.IN_REVIEW
    ).filter(assignees__in=[user])

    # number_of_cards_in_review_column = cards_in_review_column.count()

    review_feedback_cards = AgileCard.objects.filter(
        status=AgileCard.REVIEW_FEEDBACK
    ).filter(assignees__in=[user])

    in_progress_cards = AgileCard.objects.filter(status=AgileCard.IN_PROGRESS).filter(
        assignees__in=[user]
    )

    complete_cards = AgileCard.objects.filter(status=AgileCard.COMPLETE).filter(
        assignees__in=[user]
    )
    ready_cards = AgileCard.objects.filter(status=AgileCard.READY).filter(
        assignees__in=[user]
    )
    blocked_cards = AgileCard.objects.filter(status=AgileCard.BLOCKED).filter(
        assignees__in=[user]
    )

    latest_reviews = [
        o
        for o in [
            card.recruit_project.latest_review()
            for card in review_feedback_cards
            if card.recruit_project
        ]
        if o
    ]
    latest_reviews.sort(key=lambda o: o.timestamp)

    if latest_reviews:
        oldest_review_feedback_card = latest_reviews[0].timestamp.strftime(DATE_FORMAT)
    else:
        oldest_review_feedback_card = None

    project_cards = AgileCard.objects.filter(
        assignees__in=[user], content_item__content_type=ContentItem.PROJECT
    )
    # total_number_of_project_cards = project_cards.count()
    # total_weight_of_project_cards = sum_card_weights(project_cards)

    complete_projects = project_cards.filter(status=AgileCard.COMPLETE)
    # number_of_complete_project_cards = complete_projects.count()
    # weight_of_complete_project_cards = sum_card_weights(complete_projects)
    last_completed_project = (
        complete_projects.filter(recruit_project__complete_time__isnull=False)
        .order_by("recruit_project__complete_time")
        .last()
    )
    if last_completed_project:
        last_time_a_project_was_completed = (
            last_completed_project.complete_time.strftime(DATE_FORMAT)
        )
        # else:
        #     last_time_a_project_was_completed = None
    else:
        last_time_a_project_was_completed = None

    complete_projects_with_status = [
        (o, o.recruit_project.latest_review(trusted=True).status)
        for o in complete_projects
        if o.recruit_project
    ]
    excellent_complete_projects = [
        project
        for (project, status) in complete_projects_with_status
        if status == EXCELLENT
    ]
    competent_complete_projects = [
        project
        for (project, status) in complete_projects_with_status
        if status == COMPETENT
    ]

    return {
        "number_of_in_progress_cards": in_progress_cards.count(),
        "weight_of_in_progress_cards": sum_card_weights(in_progress_cards),
        "number_of_review_feedback_cards": review_feedback_cards.count(),
        "weight_of_review_feedback_cards": sum_card_weights(review_feedback_cards),
        "number_of_cards_in_review_column": cards_in_review_column.count(),
        "weight_of_cards_in_review_column": sum_card_weights(cards_in_review_column),
        "number_of_complete_cards": complete_cards.count(),
        "weight_of_complete_cards": sum_card_weights(complete_cards),
        "number_of_ready_cards": ready_cards.count(),
        "weight_of_ready_cards": sum_card_weights(ready_cards),
        "number_of_blocked_cards": blocked_cards.count(),
        "weight_of_blocked_cards": sum_card_weights(blocked_cards),
        # "number_of_complete_project_cards": number_of_complete_project_cards,
        # "weight_of_complete_project_cards": weight_of_complete_project_cards,
        # "total_number_of_project_cards": total_number_of_project_cards,
        # "total_weight_of_project_cards": total_weight_of_project_cards,
        "oldest_review_feedback_card": oldest_review_feedback_card,
        "last_time_a_project_was_completed": last_time_a_project_was_completed,
        # "too_many_cards_in_progress": number_of_in_progress_cards > 2,
        # "percent_complete_projects_by_weight": weight_of_complete_project_cards
        # / total_weight_of_project_cards
        # if total_weight_of_project_cards
        # else 0,
        "number_of_excellent_complete_project_cards": len(excellent_complete_projects),
        "weight_of_excellent_complete_project_cards": sum_card_weights(
            excellent_complete_projects
        ),
        "number_of_competent_complete_project_cards": len(competent_complete_projects),
        "weight_of_competent_complete_project_cards": sum_card_weights(
            competent_complete_projects
        ),
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


def user_as_reviewer_stats(user, cutoff):
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

    projects_reviewed_this_week = set(
        [o.recruit_project for o in reviews_done_this_week]
    )

    projects_reviewed_this_week_with_positive = [
        (o, o.recruit_project)
        for o in reviews_done_this_week.filter(
            Q(status=COMPETENT) | Q(status=EXCELLENT)
        )
    ]
    seen = []
    bad_review_projects = []
    for review, project in projects_reviewed_this_week_with_positive:
        if project in seen:
            continue
        latest_trusted_review_since = project.latest_review(
            trusted=True, timestamp_greater_than=review.timestamp
        )
        if latest_trusted_review_since and latest_trusted_review_since.status not in [
            COMPETENT,
            EXCELLENT,
        ]:
            bad_review_projects.append(project)

    return {
        "number_of_reviews_done_in_last_7_days": number_of_reviews_this_week,  # actual review instances
        "weight_of_reviews_done_in_last_7_days": weight_of_reviews_this_week,
        "number_of_cards_reviewed_in_last_7_days": len(projects_reviewed_this_week),
        "weight_of_cards_reviewed_in_last_7_days": sum_card_weights(
            projects_reviewed_this_week
        ),
        "number_of_cards_reviewed_incorrectly_in_last_7_days": len(bad_review_projects),
        "weight_of_cards_reviewed_incorrectly_in_last_7_days": sum_card_weights(
            bad_review_projects
        ),
        "number_of_cards_in_review_as_reviewer": number_of_cards_in_review_as_reviewer,
        "weight_of_cards_in_review_as_reviewer": weight_of_cards_in_review_as_reviewer,
        "oldest_card_awaiting_review": oldest_card_awaiting_review,
    }


def get_user_report(user, cutoff, extra=None):
    logger.info(f"...Processing user: {user}")
    stats = {
        "_email": user.email,
        "_id": user.id,
        "_snapshot_date": timezone.now(),
        "_employer_partner": "",
        "_last_login_time": None,
        "_start_date": None,
        "_end_date": None,
        "_percentage_of_time_spent": None,
    }

    for k, v in (extra or {}).items():
        stats[k] = v

    accumulated_user_as_reviewer_stats[
        user.id
    ] = accumulated_user_as_reviewer_stats.get(
        user.id, user_as_reviewer_stats(user, cutoff)
    )

    user_as_reviewer = accumulated_user_as_reviewer_stats[user.id]

    accumulated_user_as_assignee_stats[
        user.id
    ] = accumulated_user_as_assignee_stats.get(user.id, user_as_assignee_stats(user))
    user_as_assignee = accumulated_user_as_assignee_stats[user.id]
    for s in user_as_reviewer:
        stats[f"{AS_REVIEWER} {s}"] = user_as_reviewer[s]
    for s in user_as_assignee:
        stats[f"{AS_ASSIGNEE} {s}"] = user_as_assignee[s]

    return stats


def get_group_report(group, cutoff):
    logger.info(f"processing group: {group}")
    ret = [
        get_user_report(user=o, cutoff=cutoff, extra={"_group": group.name})
        for o in group.user_set.filter(active=True)
        # for o in TeamMembership.objects.filter(group=group, user__active=True)
    ]

    # manager_users = TeamMembership.objects.filter(
    #     group=group, user__active=True, permission_manage=True
    # )
    manager_users = []

    if ret == []:
        return ret

    numeric_values = [
        f"{AS_ASSIGNEE} number_of_complete_cards",
        f"{AS_ASSIGNEE} weight_of_complete_cards",
    ]

    # for key, value in ret[0].items():
    #     if key.startswith("_"):
    #         continue
    #     if type(value) in [int, float]:
    #         numeric_values[key] = []

    for key in numeric_values:
        values = [d[key] for d in ret]

        for d in ret:
            d[f"{key} grp tot"] = sum(values)
            d[f"{key} grp ave"] = sum(values) / len(values)
            d["_group_managers"] = ",".join([o.user.email for o in manager_users])

    return ret


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("days", type=int, nargs="?")

    def handle(self, *args, **options):
        today = timezone.now().date()
        days = options.get("days") or 7
        cutoff = timezone.now() - datetime.timedelta(days=days)

        groups = Team.objects.filter(active=True)
        all_data = []
        for group in groups:
            all_data.extend(get_group_report(group, cutoff))
            # break

        # headings = []
        # for data in all_data:
        #     headings.extend(data.keys())
        # headings = sorted(
        #     set(headings), key=lambda s: f"a{s}" if s.startswith("_") else f"b{s}"
        # )

        headings = """_email	_group_managers	_group	_employer_partner	_end_date	_id	_last_login_time	_percentage_of_time_spent	_snapshot_date	_start_date	A last_time_a_project_was_completed	A number_of_blocked_cards	A number_of_cards_in_review_column	A number_of_competent_complete_project_cards	A number_of_complete_cards	A number_of_excellent_complete_project_cards	A number_of_in_progress_cards	A number_of_ready_cards	A number_of_review_feedback_cards	A oldest_review_feedback_card	A weight_of_blocked_cards	A weight_of_cards_in_review_column	A weight_of_competent_complete_project_cards	A weight_of_complete_cards	A weight_of_complete_cards grp ave	A weight_of_complete_cards grp tot	A weight_of_excellent_complete_project_cards	A weight_of_in_progress_cards	A weight_of_ready_cards	A weight_of_review_feedback_cards	R number_of_cards_in_review_as_reviewer	R number_of_cards_reviewed_in_last_7_days	R number_of_cards_reviewed_incorrectly_in_last_7_days	R number_of_reviews_done_in_last_7_days	R oldest_card_awaiting_review	R weight_of_cards_in_review_as_reviewer	R weight_of_cards_reviewed_in_last_7_days	R weight_of_cards_reviewed_incorrectly_in_last_7_days	R weight_of_reviews_done_in_last_7_days""".split(
            "\t"
        )

        with open(
            Path(
                f"gitignore/group_report_{today.strftime('%a %d %b %Y')}__last_{days}_days.csv"
            ),
            "w",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            writer.writerows([[d[heading] for heading in headings] for d in all_data])

        # from google_helpers.utils import

        for data in all_data:
            for key in data.keys():
                if key not in headings:
                    # breakpoint()
                    pass