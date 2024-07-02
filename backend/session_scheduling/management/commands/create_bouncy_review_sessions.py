from django.core.management.base import BaseCommand
from django.utils import timezone
from session_scheduling.session_types import (
    SESSION_TROUBLESHOOT_BOUNCY_CARD,
)

from django.contrib.auth import get_user_model
from curriculum_tracking.models import RecruitProject, AgileCard
from django.db.models import Count
from sql_util.utils import SubqueryAggregate
from django.db.models import Q
from curriculum_tracking.constants import (
    RED_FLAG,
    NOT_YET_COMPETENT,
)
from session_scheduling.models import Session, SessionType

User = get_user_model()
DUE_DAYS = 14

PR_REVIEW_COUNT_THRESHOLD = 5
COMPETENCE_REVIEW_COUNT_THRESHOLD = 5


# def create_competence_review_based_sessions(self):
#     projects = (
#         RecruitProject.objects.filter(recruit_users__active=True)
#         .filter(recruit_users__groups__team__active=True)
#         .exclude(agile_card__status=AgileCard.COMPLETE)
#         .annotate(
#             negative_review_count=SubqueryAggregate(
#                 "project_reviews",
#                 filter=Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG),
#                 aggregate=Count,
#             )
#         )
#         .filter(negative_review_count__gte=COMPETENCE_REVIEW_COUNT_THRESHOLD)
#         .distinct()
#         .order_by("-negative_review_count")
#     )


def create_session_if_not_exists(project, pr_review_count, negative_review_count):

    card_id = project.agile_card.id
    assignee = project.recruit_users.first().email.split("@")[0]
    extra_title_text = f"{project.content_item.title} card_id={card_id} assignee={assignee} pr_review_count={pr_review_count} negative_review_count={negative_review_count}"

    session_type = SessionType.objects.get(name=SESSION_TROUBLESHOOT_BOUNCY_CARD)

    exists = (
        Session.objects.filter(session_type=session_type)
        .filter(created_date__gte=timezone.now() - timezone.timedelta(days=14))
        .filter(extra_title_text__contains=f"card_id={card_id} ")
        .first()
    )
    if exists:
        return

    session = Session.objects.create(
        session_type=session_type,
        due_date=timezone.now() + timezone.timedelta(days=DUE_DAYS),
        extra_title_text=extra_title_text,
        # TODO related object
        # related_object_content_type
        # related_object_id
    )
    session.attendees.set(
        project.reviewer_users.filter(is_staff=False).filter(active=True)
    )

    session.attendees.add(project.recruit_users.first())
    session.set_flavours(project.flavour_names)


def create_all_review_based_sessions():
    projects = (
        RecruitProject.objects.filter(recruit_users__active=True)
        .filter(recruit_users__email__endswith="@umuzi.org")
        .filter(recruit_users__is_staff=False)
        .filter(recruit_users__groups__team__active=True)
        .filter(agile_card__isnull=False)
        .exclude(agile_card__status=AgileCard.COMPLETE)
        .annotate(
            pr_review_count=SubqueryAggregate(
                "repository__pull_requests", aggregate=Count
            )
        )
        .annotate(
            negative_review_count=SubqueryAggregate(
                "project_reviews",
                filter=Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG),
                aggregate=Count,
            )
        )
        .filter(
            Q(pr_review_count__gte=PR_REVIEW_COUNT_THRESHOLD)
            | Q(negative_review_count__gte=COMPETENCE_REVIEW_COUNT_THRESHOLD)
        )
        .distinct()
        .prefetch_related("agile_card")
        .prefetch_related("content_item")
    )

    for project in projects:
        create_session_if_not_exists(
            project,
            pr_review_count=project.pr_review_count,
            negative_review_count=project.negative_review_count,
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_all_review_based_sessions()
        print("Done")
