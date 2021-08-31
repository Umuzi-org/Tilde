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


class OldestOpenPrUpdatedTimeTests(TestCase):
    #card = factories.AgileCardFactory()

    def setUp(self):
        self.card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.IN_PROGRESS,
        )

        self.project = RecruitProjectFactory(content_item=self.card.content_item)
        self.user = UserFactory()
        self.card.assignees.set([self.user])
        self.assertIsNotNone(self.card.recruit_project)
        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)
        self.assertEqual(self.project.content_item, self.card.content_item)
        self._reviewer_ids_since_latest_review_request = []
        self.project.review_requests_made = []

    def finding_latest_reviewer_ids(self):
        self.project.start_time = timezone.now() - timedelta(days=15)
        self.project.save()
        self.assertEqual(AgileCard.derive_status_from_project(self.project), AgileCard.IN_PROGRESS)

        # Owner of the project requests for it to be reviewed
        self.project.request_review(force_timestamp=timezone.now() - timedelta(days=10))
        self.project.review_requests_made.append(self.project.review_request_time)

        # Three reviews are made
        review_1 = factories.RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT, recruit_project=self.project
        )

        review_2 = factories.RecruitProjectReviewFactory(
            status=COMPETENT, recruit_project=self.project
        )

        review_3 = factories.RecruitProjectReviewFactory(
            status=EXCELLENT, recruit_project=self.project
        )

        if len(self.project.review_requests_made) == 0:
            return 'No review requests made and therefore no reviews submitted'
        else:
            self._reviewer_ids_since_latest_review_request.append(review_1.reviewer_user)
            self._reviewer_ids_since_latest_review_request.append(review_2.reviewer_user)
            self._reviewer_ids_since_latest_review_request.append(review_3.reviewer_user)

    @property
    def showing_latest_reviewer_ids(self):
        return self._reviewer_ids_since_latest_review_request[::1]

    def test_to_find_all_recent_reviewer_users_since_latest_review_request(self):
        self.finding_latest_reviewer_ids()
        print(self.showing_latest_reviewer_ids)