from django.core.management.base import BaseCommand
from curriculum_tracking.constants import RED_FLAG, NOT_YET_COMPETENT
from curriculum_tracking.models import AgileCard, RecruitProjectReview
from django.utils import timezone

from django.db.models import Q

from django.db.models import Count
from pathlib import Path
import csv


def get_assessment_cards():
    incomplete_assessment_cards = (
        AgileCard.objects.filter(content_item__title__startswith="Assessment:")
        .filter(~Q(status=AgileCard.COMPLETE))
        .filter(~Q(status=AgileCard.BLOCKED))
        .filter(assignees__active__in=[True])
    )

    return incomplete_assessment_cards


def get_cards_ordered_by_review():

    from sql_util.utils import SubqueryAggregate

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


headings = [
    "email",
    "teams",
    "card title",
    "flavours",
    "card status",
    "negative review count",
    "positive reviews since last review request",
    "negative reviews since last review request",
    "board url",
    "card url",
]


def make_row(card):
    negative_review_count = (
        RecruitProjectReview.objects.filter(recruit_project__agile_card=card)
        .filter(Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG))
        .count()
    )

    assignee = card.assignees.first()
    return [
        assignee.email,
        [team.name for team in assignee.teams()],
        card.content_item.title,
        card.flavour_names,
        card.status,
        negative_review_count,
        card.code_review_competent_since_last_review_request
        + card.code_review_excellent_since_last_review_request,
        card.code_review_red_flag_since_last_review_request
        + card.code_review_ny_competent_since_last_review_request,
        f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/users/{assignee.id}/board",
        f"https://tilde-front-dot-umuzi-prod.nw.r.appspot.com/card/{card.id}",
    ]


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
            writer.writerow(headings)

            total = get_assessment_cards().count()
            for i, card in enumerate(get_assessment_cards()):
                print(f"assessment card {i+1}/{total}")
                writer.writerow(make_row(card))

            total = get_cards_ordered_by_review().count()
            for i, card in enumerate(get_cards_ordered_by_review()):
                print(f"bouncey card {i+1}/{total}")
                writer.writerow(make_row(card))
