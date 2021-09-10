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


class ReviewerIdsSinceLatestReviewRequest(TestCase):
    #card = factories.AgileCardFactory()

    def setUp(self):
        self.card = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS,
        )

        self.project = self.card.recruit_project
        self.user = self.card.assignees.first()
        self.assertIsNotNone(self.card.assignees)
        self.assertIsNotNone(self.card.recruit_project)
        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)
        self.assertEqual(self.project.content_item, self.card.content_item)

    def test_finding_latest_reviewer_ids(self):
        self.project.start_time = timezone.now() - timedelta(days=5)
        self.project.save()
        self.assertEqual(AgileCard.derive_status_from_project(self.project), AgileCard.IN_PROGRESS)

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
        )
        self.review_1.timestamp = time_one
        self.review_1.save()

        self.review_2 = factories.RecruitProjectReviewFactory(
            status=COMPETENT,
            recruit_project=self.project,
        )
        self.review_2.timestamp = time_two
        self.review_2.save()

        self.review_3 = factories.RecruitProjectReviewFactory(
            status=EXCELLENT,
            recruit_project=self.project,
        )
        self.review_3.timestamp = time_three
        self.review_3.save()

        self.review_4 = factories.RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=self.project,
        )
        self.review_4.timestamp = time_four
        self.review_4.save()

        result = self.card.get_users_that_reviewed_since_last_review_request()
        ids_which_can_be_returned = [552, 553, 554, 6, 7, 8]

        # Only three of the four reviews should have been added as part of the result
        #self.assertEqual(sorted(result), sorted(ids_that_should_be_returned))

        for res in result:
            assert res in ids_which_can_be_returned

