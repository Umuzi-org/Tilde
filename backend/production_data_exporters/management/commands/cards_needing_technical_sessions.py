from django.core.management.base import BaseCommand
from curriculum_tracking.constants import (
    EXCELLENT,
    RED_FLAG,
    NOT_YET_COMPETENT,
    COMPETENT,
)
from curriculum_tracking.models import AgileCard, RecruitProjectReview
from django.utils import timezone

from django.db.models import Q, Count, Max

from pathlib import Path
import csv
from sql_util.utils import SubqueryAggregate

from datetime import timedelta


# from git_real.models import PullRequestReview
BOUNCEY_CARD_MIN_BOUNCES = 2
NO_CODE_PUSHES_MIN_DAYS = 7
CODE_PUSHES_WITH_NO_PR_MIN_DAYS = 7


def get_assessment_cards():
    incomplete_assessment_cards = (
        AgileCard.objects.filter(content_item__title__startswith="Assessment:")
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


def get_cards_with_no_pushes():
    seven_days_ago = timezone.now() - timedelta(days=CODE_PUSHES_WITH_NO_PR_MIN_DAYS)

    cards = AgileCard.objects.filter(
        Q(status=AgileCard.IN_PROGRESS) | Q(status=AgileCard.REVIEW_FEEDBACK),
        recruit_project__repository__pushes__isnull=True,
        recruit_project__repository__created_at__lte=seven_days_ago,
        assignees__active__in=[True],
    )
    return cards


def get_cards_with_pushes_no_opened_prs():
    seven_days_ago = timezone.now() - timedelta(days=CODE_PUSHES_WITH_NO_PR_MIN_DAYS)

    cards = (
        AgileCard.objects.filter(
            Q(status=AgileCard.IN_PROGRESS) | Q(status=AgileCard.REVIEW_FEEDBACK),
            recruit_project__repository__pushes__isnull=False,
            assignees__active__in=[True],
            recruit_project__repository__pull_requests__state="closed",
        )
        .annotate(
            latest_push_time=Max("recruit_project__repository__pushes__pushed_at_time")
        )
        .filter(
            latest_push_time__lte=seven_days_ago,
        )
    )

    return cards


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

    days_since_last_pr_opened = 0
    days_since_last_commit = 0
    days_since_last_push = 0

    if (
        card.status in [AgileCard.IN_PROGRESS, AgileCard.REVIEW_FEEDBACK]
        and card.recruit_project
        and card.recruit_project.repository
    ):
        commits = card.recruit_project.repository.commit_set.all()
        prs = card.recruit_project.repository.pull_requests.all()
        pushes = card.recruit_project.repository.pushes.all()

        if commits.exists():
            last_commit = commits.latest("datetime")
            time_since_last_commit = timezone.now() - last_commit.datetime
            days_since_last_commit = time_since_last_commit.days

        if prs.exists():
            latest_pr = prs.latest("created_at")
            time_since_last_pr_opened = timezone.now() - latest_pr.created_at
            days_since_last_pr_opened = time_since_last_pr_opened.days

        if pushes.exists():
            last_push = pushes.latest("pushed_at_time")
            time_since_last_push = timezone.now() - last_push.pushed_at_time
            days_since_last_push = time_since_last_push.days

    return {
        "reason": reason,
        "email": assignee.email,
        "teams": [team.name for team in assignee.teams()],
        "card title": card.content_item.title,
        "flavours": card.flavour_names,
        "card status": card.status,
        "project start time": (
            card.start_time.strftime("%d/%m/%Y") if card.start_time else ""
        ),
        "time since last commit": days_since_last_commit,
        "time since last opened pr": days_since_last_pr_opened,
        "time stuck": days_since_last_push,
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

    for i, card in enumerate(get_cards_with_no_pushes()):
        yield list(make_row(card, "no code pushes").values())

    for i, card in enumerate(get_cards_with_pushes_no_opened_prs()):
        yield list(make_row(card, "learner stuck").values())


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
                writer.writerow(row)
