from django.test import TestCase
from curriculum_tracking.tests.factories import RecruitProjectFactory
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
)
from . import factories
from core.tests.factories import UserFactory
from datetime import timedelta

from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)
from django.utils import timezone


class CreatingCardsAndReviews(TestCase):

    card = factories.AgileCardFactory(
        status=AgileCard.IN_PROGRESS,
    )

    # self.project = RecruitProjectFactory(content_item=self.card.content_item)
    # self.user = UserFactory()
    project = card.recruit_project
    user = card.assignees.first()
    card.assignees.set([user])

    project.start_time = timezone.now() - timedelta(days=15)
    project.save()

    # Owner of the project requests for it to be reviewed
    time_one = timezone.now() - timedelta(days=30)
    time_two = timezone.now() - timedelta(days=20)
    time_three = timezone.now() - timedelta(days=10)
    project.request_review(force_timestamp=time_two)


    # Three reviews are made
    review_1 = factories.RecruitProjectReviewFactory(
        status=NOT_YET_COMPETENT,
        recruit_project=project,
        timestamp=time_one
    )

    review_2 = factories.RecruitProjectReviewFactory(
        status=COMPETENT,
        recruit_project=project,
        timestamp=time_two
    )

    review_3 = factories.RecruitProjectReviewFactory(
        status=EXCELLENT,
        recruit_project=project,
        timestamp=time_three
    )