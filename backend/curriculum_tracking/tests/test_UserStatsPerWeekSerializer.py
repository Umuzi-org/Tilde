from git_real.models import PullRequestReview
from curriculum_tracking.serializers import UserStatsPerWeekSerializer
from django.test import TestCase
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
)
from . import factories
from social_auth.tests.factories import SocialProfileFactory
from datetime import timedelta
from git_real.tests import factories as git_real_factories

from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
    COMPETENT,
)
from curriculum_tracking.tests.factories import (
    ContentItemFactory,
    AgileCardFactory,
    RecruitProjectReviewFactory,
)
from django.utils import timezone


class TestingForTheStatsAPI(TestCase):

    def setUp(self):
        self.card_1 = AgileCardFactory(
            status=AgileCard.IN_PROGRESS,
        )

        self.project_1 = self.card_1.recruit_project
        self.user = self.card_1.assignees.first()
        self.project_1.start_time = timezone.now() - timedelta(days=5)
        self.project_1.save()

        # Will use this repo card, PR, today, yesterday, two_days_before_yesterday and two_weeks_ago later on
        # in test 'test_pr_reviews_card_in_different_column_due_to_review_status'.
        self.today = timezone.now()
        self.yesterday = self.today - timezone.timedelta(days=1)
        self.two_days_before_yesterday = self.today - timezone.timedelta(days=3)
        self.two_weeks_ago = self.today - timezone.timedelta(days=14)

        self.repo_card_one = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS
        )
        self.repo_card_one.recruit_project.repository = git_real_factories.RepositoryFactory()
        self.repo_card_one.save()

        self.pull_request = git_real_factories.PullRequestFactory(
            repository=self.repo_card_one.recruit_project.repository, updated_at=self.today
        )
        self.pull_request.save()

    def test_one_card_in_progress_before_any_reviews(self):

        # One card, no reviews just yet, function 'get_cards_in_progress_column' should return one card
        self.assertEqual(self.card_1.status, AgileCard.IN_PROGRESS)
        self.assertEqual(self.project_1.content_item, self.card_1.content_item)
        self.assertEqual(AgileCard.derive_status_from_project(self.project_1), AgileCard.IN_PROGRESS)
        self.assertEqual(
            UserStatsPerWeekSerializer.get_cards_in_progress_column(UserStatsPerWeekSerializer, User=self.user), 1
        )

    def test_one_card_in_review_feedback_column(self):

        # Request for a review to happen on project_1, card_1
        request_review_time = self.project_1.start_time + timedelta(1)
        time_one = self.project_1.start_time - timedelta(days=6)
        self.project_1.request_review(force_timestamp=request_review_time)
        review_1 = RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=self.project_1,
            timestamp=time_one
        )
        review_1.timestamp = time_one
        review_1.save()

        # review_1 had a status of NYC, so we should have at least one card in the 'REVIEW FEEDBACK' column
        self.assertEqual(UserStatsPerWeekSerializer.get_cards_in_review_feedback_column(
            UserStatsPerWeekSerializer, User=self.user), 1
        )

    def test_no_card_in_completed_column_after_competent_review_reviewer_not_trusted_reviewer(self):
        time_two = self.project_1.start_time + timedelta(days=4)
        review_2 = RecruitProjectReviewFactory(
            status=COMPETENT,
            recruit_project=self.project_1,
        )
        review_2.timestamp = time_two
        review_2.save()

        # review_2 had a status of COMPETENT, the reviewer is not trusted and therefore we should have zero cards in
        # the completed column
        self.assertEqual(UserStatsPerWeekSerializer.get_cards_in_completed_column(
            UserStatsPerWeekSerializer, User=self.user), 0
        )

    def test_one_card_started_in_the_past_seven_days(self):
        self.assertEqual(UserStatsPerWeekSerializer.get_cards_started_last_7_days(
            UserStatsPerWeekSerializer, User=self.user), 1
        )

    def test_no_cards_completed_in_past_seven_days(self):

        self.assertEqual(UserStatsPerWeekSerializer.get_cards_completed_last_7_days(
            UserStatsPerWeekSerializer, User=self.user), 0
        )

    def test_one_card_in_complete_column(self):

        content_item_2 = ContentItemFactory(
            content_type=ContentItem.TOPIC,
            project_submission_type=ContentItem.REPOSITORY,
        )
        card_2 = AgileCardFactory(
            content_item=content_item_2,
            status=AgileCard.COMPLETE,
        )
        assigned_person = SocialProfileFactory().user
        card_2.assignees.set([assigned_person])

        # We should have at least one card in the completed column and since it went there within the last seven days
        # the function 'get_cards_completed_last_7_days' should also return at least one card
        self.assertEqual(UserStatsPerWeekSerializer.get_cards_in_completed_column(
            UserStatsPerWeekSerializer, User=assigned_person), 1
        )
        self.assertEqual(UserStatsPerWeekSerializer.get_cards_completed_last_7_days(
            UserStatsPerWeekSerializer, User=assigned_person), 1
        )

    def test_cards_in_the_review_column_waiting_for_a_review(self):

        # Two cards in the IN_REVIEW column
        content_item_3 = ContentItemFactory(
            content_type=ContentItem.TOPIC,
            project_submission_type=ContentItem.REPOSITORY,
        )

        card_3 = AgileCardFactory(
            content_item=content_item_3,
            status=AgileCard.IN_REVIEW,
            recruit_project=None,
        )

        card_4 = AgileCardFactory(
            content_item=content_item_3,
            status=AgileCard.IN_REVIEW,
            recruit_project=None,
        )

        assigned_person = SocialProfileFactory().user
        card_3.assignees.set([assigned_person])
        card_4.assignees.set([assigned_person])

        # We should get two cards in the review column waiting for a review
        self.assertEqual(UserStatsPerWeekSerializer.get_cards_in_review_column(
            UserStatsPerWeekSerializer, User=assigned_person), 2
        )

    def test_pr_reviews_card_in_different_column_due_to_review_status(self):

        # Now creating reviews on the PR
        factories.PullRequestReviewFactory(
            id=1,
            submitted_at=self.today,
            commit_id=self.repo_card_one.assignees.first().id
        )

        factories.PullRequestReviewFactory(
            id=2,
            submitted_at=self.yesterday,
            commit_id=self.repo_card_one.assignees.first().id
        )

        factories.PullRequestReviewFactory(
            id=3,
            submitted_at=self.two_days_before_yesterday,
            commit_id=self.repo_card_one.assignees.first().id
        )

        factories.PullRequestReviewFactory(
            id=4,
            submitted_at=self.two_weeks_ago,
            commit_id=self.repo_card_one.assignees.first().id
        )

        # Four PR reviews were done to date, so we should get a value of 4 for the particular user
        self.assertEqual(UserStatsPerWeekSerializer.get_total_number_of_pr_reviews(
            UserStatsPerWeekSerializer, self.repo_card_one.assignees.first()), 4
        )

        # Four PR reviews were done but only three of them were done in the last seven days so we should get a value
        # of 3
        self.assertEqual(UserStatsPerWeekSerializer.get_pr_reviews_done_last_7_days(
            UserStatsPerWeekSerializer, self.repo_card_one.assignees.first()), 3
        )