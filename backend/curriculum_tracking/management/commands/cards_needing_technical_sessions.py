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
from django.db.models import Sum, F
from sql_util.utils import SubqueryAggregate

# from git_real.models import PullRequestReview


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
        .filter(negative_review_count__gt=2)
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

    positive_review_count = (
        RecruitProjectReview.objects.filter(recruit_project__agile_card=card)
        .filter(Q(status=COMPETENT) | Q(status=EXCELLENT))
        .count()
    )

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
    return {
        "reason": reason,
        "email": assignee.email,
        "teams": [team.name for team in assignee.teams()],
        "card title": card.content_item.title,
        "flavours": card.flavour_names,
        "card status": card.status,
        "staff_who_think_its_competent": "\n".join(staff_who_think_its_competent),
        "total negative review count": negative_review_count,
        "total positive review count": positive_review_count,
        "positive reviews since last review request": card.code_review_competent_since_last_review_request
        + card.code_review_excellent_since_last_review_request,
        "negative reviews since last review request": card.code_review_red_flag_since_last_review_request
        + card.code_review_ny_competent_since_last_review_request,
        "board url": f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/users/{assignee.id}/board",
        "card url": f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card.id}",
    }


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
            assessment_cards = get_assessment_cards()
            headings = list(make_row(assessment_cards.first(), "").keys())
            writer.writerow(headings)

            cards_ordered_by_pr_changes_requested = (
                get_cards_ordered_by_pr_change_requests()
            )

            total = cards_ordered_by_pr_changes_requested.count()
            for i, card in enumerate(cards_ordered_by_pr_changes_requested):
                print(f"pr card {i+1}/{total}")
                writer.writerow(list(make_row(card, "pr change requested").values()))

            total = assessment_cards.count()
            for i, card in enumerate(assessment_cards):
                print(f"assessment card {i+1}/{total}")
                writer.writerow(list(make_row(card, "Assessment sessions").values()))

            total = get_cards_ordered_by_review().count()
            for i, card in enumerate(get_cards_ordered_by_review()):
                print(f"bouncy card {i+1}/{total}")
                writer.writerow(list(make_row(card, "bouncy card").values()))
