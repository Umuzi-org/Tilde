from django.test import TestCase
from curriculum_tracking.models import AgileCard
from . import factories
from datetime import timedelta

from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)
from django.utils import timezone


class OldestOpenPrUpdatedTimeTests(TestCase):
    #card = factories.AgileCardFactory()

    def setUp(self):
        self.card = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS,
        )

        self.project = self.card.recruit_project
        self.user = self.card.assignees.first()
        self.card.assignees.set([self.user])
        self.assertIsNotNone(self.card.recruit_project)
        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)
        self.assertEqual(self.project.content_item, self.card.content_item)

    def test_finding_latest_reviewer_ids(self):
        self.project.start_time = timezone.now() - timedelta(days=5)
        self.project.save()
        self.assertEqual(AgileCard.derive_status_from_project(self.project), AgileCard.IN_PROGRESS)

        """The review done on time_one should be excluded since it was done before the project owner
        requested for the project to be reviewed."""
        request_review_time = self.project.start_time + timedelta(1)
        self.project.request_review(force_timestamp=request_review_time)
        time_one = self.project.start_time - timedelta(days=6)
        time_two = self.project.start_time + timedelta(days=4)
        time_three = self.project.start_time + timedelta(days=3)
        time_four = self.project.start_time + timedelta(days=2)

        # Four reviews are made at different times
        self.review_1 = factories.RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=self.project,
            timestamp=time_one
        )

        self.review_2 = factories.RecruitProjectReviewFactory(
            status=COMPETENT,
            recruit_project=self.project,
            timestamp=time_two
        )

        self.review_3 = factories.RecruitProjectReviewFactory(
            status=EXCELLENT,
            recruit_project=self.project,
            timestamp=time_three
        )

        self.review_4 = factories.RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=self.project,
            timestamp=time_four
        )

        self.project.save()
        result = self.card.get_users_that_reviewed_since_last_review_request()

        # Only three of the reviews should have been added as part of the result
        self.assertNotEqual(len(result), 4)
        print(result)

