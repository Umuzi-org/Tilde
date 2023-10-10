from django.core.management.base import BaseCommand
from curriculum_tracking.constants import (
    EXCELLENT,
    RED_FLAG,
    NOT_YET_COMPETENT,
    COMPETENT,
)
from curriculum_tracking.models import AgileCard, RecruitProjectReview
from django.utils import timezone

from django.db.models import Q

from django.db.models import Count
from pathlib import Path
import csv
from sql_util.utils import SubqueryAggregate


# TODO: get current script working locally - done
# TODO: add demo data for validating if everything works - done
# TODO: add more demo data for validating if everything works
# TODO: add cards that are IP/RF without pushes for more than 7 days
# TODO: add cards that are IP/RF without pushes without opening a PR
# TODO: add a start time column - done
# TODO: add a time since last commit column
# TODO: add a time since last PR opened column

# from git_real.models import PullRequestReview
BOUNCEY_CARD_MIN_BOUNCES = 2


def get_assessment_cards():
    incomplete_assessment_cards = (
        AgileCard.objects.filter(content_item__title__startswith="Assessment:")
        # .annotate(
        #     positive_review_count=Sum(
        #         F("recruit_project__code_review_competent_since_last_review_request"),
        #         F("recruit_project__code_review_excellent_since_last_review_request"),
        #     )
        # )
        # .extra(
        #     select={
        #         "positive_review_count": "code_review_competent_since_last_review_request + code_review_excellent_since_last_review_request"
        #     }
        # )
        .filter(~Q(status=AgileCard.COMPLETE))
        .filter(~Q(status=AgileCard.BLOCKED))
        .filter(assignees__active__in=[True])
        .order_by("recruit_project__code_review_competent_since_last_review_request")
    )

    return incomplete_assessment_cards


def get_cards_ordered_by_review():
    return (
        AgileCard.objects.filter(~Q(status=AgileCard.COMPLETE))
        .filter(assignees__active__in=[True])
        .filter(~Q(content_item__title__startswith="Assessment:"))
        .annotate(
            negative_review_count=SubqueryAggregate(
                "recruit_project__project_reviews",
                filter=Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG),
                aggregate=Count,
            )
        )
        .filter(negative_review_count__gt=BOUNCEY_CARD_MIN_BOUNCES)
        .order_by("-negative_review_count")
    )


def get_cards_ordered_by_pr_change_requests():
    return (
        AgileCard.objects.filter(
            Q(status=AgileCard.IN_PROGRESS) | Q(status=AgileCard.REVIEW_FEEDBACK)
        )
        .filter(assignees__active__in=[True])
        .annotate(
            pr_change_requests=SubqueryAggregate(
                "recruit_project__repository__pull_requests__reviews",
                filter=Q(state="CHANGES_REQUESTED"),
                aggregate=Count,
            )
        )
        .filter(pr_change_requests__gte=3)
        .order_by("pr_change_requests")
    )


def make_row(card, reason):
    negative_review_count = (
        RecruitProjectReview.objects.filter(recruit_project__agile_card=card)
        .filter(Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG))
        .count()
    )

    positive_reviews = (
        RecruitProjectReview.objects.filter(recruit_project__agile_card=card)
        .filter(Q(status=COMPETENT) | Q(status=EXCELLENT))
        .order_by("timestamp")
        .prefetch_related("reviewer_user")
    )

    positive_review_count = positive_reviews.count()

    if card.status == AgileCard.IN_REVIEW:
        project = card.recruit_project
        reviews = project.project_reviews.filter(
            timestamp__gt=project.review_request_time
        ).filter(Q(status=COMPETENT) | Q(status=EXCELLENT))
        staff_who_think_its_competent = [
            review.reviewer_user.email
            for review in reviews
            if review.reviewer_user.is_staff
        ]
    else:
        staff_who_think_its_competent = []

    assignee = card.assignees.first()

    positive_reviewer_emails = []
    for review in positive_reviews:
        reviewer_user = review.reviewer_user
        if not reviewer_user.active:
            continue
        email = reviewer_user.email
        if email not in positive_reviewer_emails:
            positive_reviewer_emails.append(email)

    return {
        "reason": reason,
        "email": assignee.email,
        "teams": [team.name for team in assignee.teams()],
        "card title": card.content_item.title,
        "flavours": card.flavour_names,
        "card status": card.status,
        "project start time": card.start_time.strftime("%d/%m/%Y %H:%M:%S")
        if card.start_time
        else "",
        "staff_who_think_its_competent": "\n".join(staff_who_think_its_competent),
        "total negative review count": negative_review_count,
        "total positive review count": positive_review_count,
        "positive reviews since last review request": card.code_review_competent_since_last_review_request
        + card.code_review_excellent_since_last_review_request,
        "negative reviews since last review request": card.code_review_red_flag_since_last_review_request
        + card.code_review_ny_competent_since_last_review_request,
        "board url": f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/users/{assignee.id}/board",
        "card url": f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card.id}",
        "positive reviewer emails in order": "\n".join(positive_reviewer_emails),
    }


def get_all_csv_rows():
    assessment_cards = get_assessment_cards()
    headings = list(make_row(assessment_cards.first(), "").keys())
    yield headings

    cards_ordered_by_pr_changes_requested = get_cards_ordered_by_pr_change_requests()

    # total = cards_ordered_by_pr_changes_requested.count()
    for i, card in enumerate(cards_ordered_by_pr_changes_requested):
        # print(f"pr card {i+1}/{total}")
        yield list(make_row(card, "pr change requested").values())

    # total = assessment_cards.count()
    for i, card in enumerate(assessment_cards):
        # print(f"assessment card {i+1}/{total}")
        yield list(make_row(card, "Assessment sessions").values())

    # total = get_cards_ordered_by_review().count()
    for i, card in enumerate(get_cards_ordered_by_review()):
        # print(f"bouncy card {i+1}/{total}")
        yield list(make_row(card, "bouncy card").values())


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = timezone.now().date()

        with open(
            Path(
                f"gitignore/cards_needing_technical_sessions_{today.strftime('%a %d %b %Y')}.csv",
            ),
            "w",
        ) as f:
            writer = csv.writer(f)
            for row in get_all_csv_rows():
                print("@", row)
                writer.writerow(row)
