"""
python manage.py create_fake_data sheena.oconnell@umuzi.org sheena.oconnell@gmail.com sheena@prelude.tech sheenarbw sheenarbw2
"""

from django.core.management.base import BaseCommand
from core.tests.factories import UserFactory, CohortFactory, RecruitCohortFactory
from curriculum_tracking.tests.factories import AgileCardFactory, ContentItemFactory
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
    RecruitProject,
)
from social_auth.models import SocialProfile
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from core.models import (
    UserGroup,
    UserGroupMembership,
    User,
    RecruitCohort,
    EmployerPartner,
)

User = get_user_model()


def create_superuser(email):
    user, _ = User.objects.get_or_create(email=email)
    user.is_superuser = True
    user.is_staff = True
    user.set_password(email)
    user.save()
    return user


def create_recruit(cohort, email):
    user, _ = User.objects.get_or_create(email=email)

    employer = EmployerPartner.objects.get_or_create(name="test employer")[0]

    RecruitCohort.objects.get_or_create(
        user=user,
        defaults={
            "cohort": cohort,
            "start_date": cohort.start_date,
            "end_date": cohort.end_date,
            "employer_partner": employer,
        },
    )

    return user


def create_cards(recruit1, recruit2):
    [create_topic_cards(recruit1) for i in range(5)]
    [create_project_cards(recruit1, recruit2) for i in range(5)]
    [create_workshop_card(recruit1) for i in range(2)]


def create_project_cards(recruit1, recruit2):
    cards = [
        make_card(ContentItem.PROJECT, project_submission_type=ContentItem.REPOSITORY),
        make_card(ContentItem.PROJECT, project_submission_type=ContentItem.LINK),
    ]
    cards.append(
        make_card(
            ContentItem.PROJECT,
            project_submission_type=ContentItem.CONTINUE_REPO,
            continue_from_repo=cards[0].content_item,
        )
    )
    for card in cards:
        card.assignees.add(recruit1)
        card.reviewers.add(recruit2)


def create_workshop_card(recruit1):
    card = make_card(ContentItem.WORKSHOP)
    card.assignees.add(recruit1)


def create_topic_cards(recruit1):
    card = make_card(ContentItem.TOPIC, topic_needs_review=True)
    card.assignees.add(recruit1)
    card = make_card(ContentItem.TOPIC, topic_needs_review=False)
    card.assignees.add(recruit1)


def make_card(
    content_type,
    project_submission_type=None,
    continue_from_repo=None,
    topic_needs_review=False,
    recruit_users=[],
    reviewer_users=[],
):
    assert recruit_users
    assert reviewer_users
    if content_type == ContentItem.PROJECT:
        content_item = ContentItemFactory(
            content_type=content_type,
            project_submission_type=project_submission_type,
            continue_from_repo=continue_from_repo,
        )
        recruit_project = RecruitProject.objects.create(content_item=content_item,)
        recruit_project.recruit_users.set(recruit_users)
        recruit_project.reviewer_users.set(reviewer_users)

        return AgileCardFactory(
            content_item=content_item,
            status=AgileCard.READY,
            recruit_project=recruit_project,
        )

    else:
        content_item = ContentItemFactory(
            content_type=content_type, topic_needs_review=topic_needs_review,
        )

        return AgileCardFactory(content_item=content_item, status=AgileCard.READY,)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("superuser", type=str)
        parser.add_argument("recruit1", type=str)
        parser.add_argument("recruit2", type=str)
        parser.add_argument("github1", type=str)
        parser.add_argument("github2", type=str)

    def handle(self, *args, **options):
        user = create_superuser(options["superuser"])

        SocialProfile.objects.get_or_create(
            user=user, defaults={"github_name": options["github1"]}
        )

        cohort = CohortFactory()

        recruit1 = create_recruit(cohort, options["recruit1"])
        SocialProfile.objects.get_or_create(
            user=recruit1, defaults={"github_name": options["github2"]}
        )
        recruit2 = create_recruit(cohort, options["recruit2"])

        create_cards(recruit1, recruit2)

        group, _ = UserGroup.objects.get_or_create(name="group1")

        for recruit in [recruit1, recruit2]:
            UserGroupMembership.objects.get_or_create(
                user=recruit,
                group=group,
                permission_student=True,
                permission_view=False,
                permission_manage=False,
            )
