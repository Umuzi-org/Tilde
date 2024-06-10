"""
If learners failed a recent level 0 or level 1 CB test, they need one of these
"""

from django.core.management.base import BaseCommand
from session_scheduling.models import Session, SessionType
from session_scheduling.session_types import SESSION_PROBLEM_SOLVING_FOUNDATION_SESSION
from coderbyte_tests.models import CoderbyteTestResult
from django.db.models import Q
from django.db.models import OuterRef, Subquery
from ..helpers import group_learners
from django.utils import timezone
from curriculum_tracking.models import AgileCard

# from coderbyte_tests.constants import PROBLEM_SOLVING_TEAM_NAME_START

# User = get_user_model()

DUE_DAYS = 21
GROUP_SIZE = 3


def get_most_recent_test_results():
    """get the most recent test for each learner and work from that"""
    subquery = Subquery(
        CoderbyteTestResult.objects.filter(
            Q(status=CoderbyteTestResult.STATUS_SUBMITTED)
            | Q(status=CoderbyteTestResult.STATUS_TIME_EXPIRED)
        )
        .filter(
            Q(assessment_name__startswith=f"Problem solving")
            | Q(assessment_name__startswith=f"Cloned Problem solving")
        )
        .filter(user_id=OuterRef("user_id"))
        .order_by("-date_joined")
        .values_list("id", flat=True)[:1]
    )

    all_results = CoderbyteTestResult.objects.filter(user__active=True).filter(
        id__in=subquery
    )
    return all_results


def get_users_who_failed(level):
    fails = (
        get_most_recent_test_results()
        .filter(
            Q(assessment_name__startswith=f"Problem solving {level}")
            | Q(assessment_name__startswith=f"Cloned Problem solving {level}")
        )
        .filter(final_score__lte=50)
        .prefetch_related("user")
    )
    return [o.user for o in fails]


def create_session(learners, level, language):
    session_type = SessionType.objects.get(
        name=SESSION_PROBLEM_SOLVING_FOUNDATION_SESSION
    )
    session = Session.objects.create(
        session_type=session_type,
        due_date=timezone.now() + timezone.timedelta(days=DUE_DAYS),
        extra_title_text=str(level),
    )
    for user in learners:
        session.attendees.add(user)
    session.set_flavours([language])


def group_users_by_main_language(users):
    result = {}
    for user in users:
        card = AgileCard.objects.filter(
            content_item_id=709, assignees=user
        ).first()  # functions, returns and printing to the terminal
        if card:
            flavour = " ".join(card.flavour_names)
            result[flavour] = result.get(flavour, [])
            result[flavour].append(user)
    return result


def create_psf_sessions():
    for level in [0, 1]:
        failed_users = get_users_who_failed(level)
        users_by_main_language = group_users_by_main_language(failed_users)

        for language, users in users_by_main_language.items():
            groups = group_learners(users, GROUP_SIZE)
            for group in groups:
                create_session(group, level, language)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_psf_sessions()
        print("Done")
