from curriculum_tracking.tests.factories import (
    ContentItemFactory,
    AgileCardFactory,
    RecruitProjectReviewFactory,
)
from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
    RecruitProject,
)
from social_auth.tests.factories import SocialProfileFactory, GithubOAuthTokenFactory
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase


class CreatingDataForTesting(TestCase):

    def test_creating_cards(self):
        # One card with 4 reviews to follow on it
        self.card_1 = AgileCardFactory(
            status=AgileCard.IN_PROGRESS,
        )

        self.project_1 = self.card_1.recruit_project
        self.user = self.card_1.assignees.first()
        assert self.card_1.status == AgileCard.IN_PROGRESS
        assert self.project_1.content_item == self.card_1.content_item

        self.project_1.start_time = timezone.now() - timedelta(days=5)
        self.project_1.save()
        assert AgileCard.derive_status_from_project(self.project_1) == AgileCard.IN_PROGRESS

        self.request_review_time = self.project_1.start_time + timedelta(1)
        self.project_1.request_review(force_timestamp=self.request_review_time)
        time_one = self.project_1.start_time - timedelta(days=6)
        time_two = self.project_1.start_time + timedelta(days=4)
        time_three = self.project_1.start_time + timedelta(days=3)
        time_four = self.project_1.start_time + timedelta(days=2)


        # Four reviews are made at different times
        self.review_1 = RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=self.project_1,
            timestamp=time_one
        )
        self.review_1.timestamp = time_one
        self.review_1.save()

        self.review_2 = RecruitProjectReviewFactory(
            status=COMPETENT,
            recruit_project=self.project_1,
        )
        self.review_2.timestamp = time_two
        self.review_2.save()

        self.review_3 = RecruitProjectReviewFactory(
            status=EXCELLENT,
            recruit_project=self.project_1,
        )
        self.review_3.timestamp = time_three
        self.review_3.save()

        self.review_4 = RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=self.project_1,
        )
        self.review_4.timestamp = time_four
        self.review_4.save()


        # Three cards in the IN_PROGRESS column
        self.content_item = ContentItemFactory(
            content_type=ContentItem.PROJECT,
            project_submission_type=ContentItem.REPOSITORY,
        )

        self.card_2 = AgileCardFactory(
            content_item=self.content_item,
            status=AgileCard.IN_PROGRESS,
            recruit_project=None,
        )

        self.card_3 = AgileCardFactory(
            content_item=self.content_item,
            status=AgileCard.IN_PROGRESS,
            recruit_project=None,
        )

        self.card_4 = AgileCardFactory(
            content_item=self.content_item,
            status=AgileCard.IN_PROGRESS,
            recruit_project=None,
        )

        assignee = SocialProfileFactory().user
        self.card_2.assignees.set([assignee])
        self.card_3.assignees.set([assignee])
        self.card_4.assignees.set([assignee])

        #self.card_2.start_project()
        #self.card_3.start_project()
        #self.card_4.start_project()

        # Four cards in the COMPLETE column
        self.content_item_2 = ContentItemFactory(
            content_type=ContentItem.TOPIC,
            project_submission_type=ContentItem.REPOSITORY,
        )

        self.card_5 = AgileCardFactory(
            content_item=self.content_item_2,
            status=AgileCard.COMPLETE,
            #recruit_project=None,
        )

        self.card_6 = AgileCardFactory(
            content_item=self.content_item_2,
            status=AgileCard.COMPLETE,
            #recruit_project=None,
        )

        self.card_7 = AgileCardFactory(
            content_item=self.content_item_2,
            status=AgileCard.COMPLETE,
            #recruit_project=None,
        )

        self.card_8 = AgileCardFactory(
            content_item=self.content_item_2,
            status=AgileCard.COMPLETE,
            #recruit_project=None,
        )

        assignee_ = SocialProfileFactory().user
        self.card_5.assignees.set([assignee_])
        self.card_6.assignees.set([assignee_])
        self.card_7.assignees.set([assignee_])
        self.card_8.assignees.set([assignee_])


        # Two cards in the IN_REVIEW column
        self.content_item_3 = ContentItemFactory(
            content_type=ContentItem.TOPIC,
            project_submission_type=ContentItem.REPOSITORY,
        )

        self.card_9 = AgileCardFactory(
            content_item=self.content_item_3,
            status=AgileCard.IN_REVIEW,
            recruit_project=None,
        )

        self.card_10 = AgileCardFactory(
            content_item=self.content_item_3,
            status=AgileCard.IN_REVIEW,
            recruit_project=None,
        )

        assignee_ = SocialProfileFactory().user
        self.card_9.assignees.set([assignee_])
        self.card_10.assignees.set([assignee_])