import unittest
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
)
from social_auth.tests.factories import SocialProfileFactory
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from . import factories
from git_real.tests import factories as git_real_factories
from git_real.models import PullRequestReview
from core.models import User
from curriculum_tracking.serializers import UserStatsPerWeekSerializer


class TestingForTheStatsAPI(TestCase):

    def test_creating_cards_and_testing_functionality_of_stats_api(self):

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

        request_review_time = self.project_1.start_time + timedelta(1)
        self.project_1.request_review(force_timestamp=request_review_time)
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

        # One card in the IN_PROGRESS column
        self.content_item = ContentItemFactory(
            content_type=ContentItem.REPOSITORY,
            project_submission_type=ContentItem.REPOSITORY,
        )
        self.card_5 = AgileCardFactory(
            content_item=self.content_item,
            status=AgileCard.IN_PROGRESS
        )
        self.assignee = SocialProfileFactory().user
        self.card_5.assignees.set([self.assignee])

        # One card in the COMPLETE column
        self.content_item_2 = ContentItemFactory(
            content_type=ContentItem.TOPIC,
            project_submission_type=ContentItem.REPOSITORY,
        )
        self.card_6 = AgileCardFactory(
            content_item=self.content_item_2,
            status=AgileCard.COMPLETE,
        )
        self.assignee__ = SocialProfileFactory().user
        self.card_6.assignees.set([self.assignee__])

        self.assertIsNotNone(UserStatsPerWeekSerializer.get_cards_in_completed_column(UserStatsPerWeekSerializer, self.assignee__))
        self.assertIsNotNone(UserStatsPerWeekSerializer.get_cards_completed_last_7_days(UserStatsPerWeekSerializer, self.assignee__))
        assert UserStatsPerWeekSerializer.get_cards_in_completed_column(UserStatsPerWeekSerializer, self.assignee__) == 1
        assert UserStatsPerWeekSerializer.get_cards_completed_last_7_days(UserStatsPerWeekSerializer, self.assignee__) == 1

        # Two cards in the IN_REVIEW column
        self.content_item_3 = ContentItemFactory(
            content_type=ContentItem.TOPIC,
            project_submission_type=ContentItem.REPOSITORY,
        )

        self.card_7 = AgileCardFactory(
            content_item=self.content_item_3,
            status=AgileCard.IN_REVIEW,
            recruit_project=None,
        )

        self.card_8 = AgileCardFactory(
            content_item=self.content_item_3,
            status=AgileCard.IN_REVIEW,
            recruit_project=None,
        )

        self.assignee_ = SocialProfileFactory().user
        self.card_7.assignees.set([self.assignee_])
        self.card_8.assignees.set([self.assignee_])

        self.assertIsNotNone(UserStatsPerWeekSerializer.get_cards_in_review_column(UserStatsPerWeekSerializer, self.assignee_))
        assert UserStatsPerWeekSerializer.get_cards_in_review_column(UserStatsPerWeekSerializer, self.assignee_) == 2
        self.assertIsNotNone(UserStatsPerWeekSerializer.get_cards_in_progress_column(UserStatsPerWeekSerializer, self.assignee_))
        assert UserStatsPerWeekSerializer.get_cards_in_progress_column(UserStatsPerWeekSerializer, self.assignee_) == 0
        self.assertIsNotNone(UserStatsPerWeekSerializer.get_cards_in_progress_column(UserStatsPerWeekSerializer, self.assignee))
        assert UserStatsPerWeekSerializer.get_cards_in_progress_column(UserStatsPerWeekSerializer, self.assignee) == 1
        self.assertIsNotNone(UserStatsPerWeekSerializer.get_cards_in_review_feedback_column(UserStatsPerWeekSerializer, self.user))
        assert UserStatsPerWeekSerializer.get_cards_in_review_feedback_column(UserStatsPerWeekSerializer, self.user) == 1

        """
        # Create four cards and open a PR on each of them
        today = timezone.now()
        yesterday = today - timezone.timedelta(days=1)
        day_before_yesterday = today - timezone.timedelta(days=2)
        two_days_before_yesterday = today - timezone.timedelta(days=3)
        two_weeks_ago = today - timezone.timedelta(days=14)

        self.repo_card_one = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS
        )
        self.repo_card_one.recruit_project.repository = git_real_factories.RepositoryFactory()
        self.repo_card_one.save()

        self.repo_card_two = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS
        )
        self.repo_card_two.recruit_project.repository = git_real_factories.RepositoryFactory()
        self.repo_card_two.save()

        self.repo_card_three = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS
        )
        self.repo_card_three.recruit_project.repository = git_real_factories.RepositoryFactory()
        self.repo_card_three.save()

        self.repo_card_four = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS
        )
        self.repo_card_four.recruit_project.repository = git_real_factories.RepositoryFactory()
        self.repo_card_four.save()


        self.pr_yesterday = git_real_factories.PullRequestFactory(
            repository=self.repo_card_one.recruit_project.repository, updated_at=yesterday
        )

        self.pr_today = git_real_factories.PullRequestFactory(
            repository=self.repo_card_one.recruit_project.repository, updated_at=today
        )

        self.pr_day_before_yesterday = git_real_factories.PullRequestFactory(
            repository=self.repo_card_one.recruit_project.repository, updated_at=day_before_yesterday
        )

        self.pr_two_days_before_yesterday = git_real_factories.PullRequestFactory(
            repository=self.repo_card_one.recruit_project.repository, updated_at=two_days_before_yesterday
        )

        self.pr_yesterday.save()
        self.pr_today.save()
        self.pr_two_days_before_yesterday.save()
        self.pr_day_before_yesterday.save()


        # Now creating reviews on the PR's

        pr_review_for_pr_today = PullRequestReview.objects.create(
            html_url="https://github.com/Umuzi-org/PullRequest-Review(1)",
            pull_request_id=self.pr_today.id,
            author_github_name="DeadManWalking",
            submitted_at=today,
            body="A horse walks into a bar, the barman says 'Why the long face?'",
            commit_id=self.repo_card_one.assignees.first().id,
            state="closed",
            user_id=self.repo_card_one.assignees.first().id
        )
        pr_review_for_pr_today.save()

        pr_review_for_pr_yesterday = PullRequestReview.objects.create(
            html_url="https://github.com/Umuzi-org/PullRequest-Review(2)",
            pull_request_id=self.pr_yesterday.id,
            author_github_name="DeadManWalking",
            submitted_at=yesterday,
            body="A horse walks into a bar, the barman says 'Why the long face?'",
            commit_id=self.repo_card_one.assignees.first().id,
            state="closed",
            user_id=self.repo_card_one.assignees.first().id
        )
        pr_review_for_pr_yesterday.save()

        pr_review_two_weeks_ago = PullRequestReview.objects.create(
            html_url="https://github.com/Umuzi-org/PullRequest-Review(3)",
            pull_request_id=self.pr_today.id,
            author_github_name="DeadManWalking",
            submitted_at=two_weeks_ago,
            body="This review happened a long time ago.",
            commit_id=self.repo_card_one.assignees.first().id,
            state="closed",
            user_id=self.repo_card_one.assignees.first().id
        )
        pr_review_two_weeks_ago.save()

        pr_review_two_days_before_yesterday = PullRequestReview.objects.create(
            html_url="https://github.com/Umuzi-org/PullRequest-Review(4)",
            pull_request_id=self.pr_two_days_before_yesterday.id,
            author_github_name="DeadManWalking",
            submitted_at=two_days_before_yesterday,
            body="This review happened no more than two days ago",
            commit_id=self.repo_card_one.assignees.first().id,
            state="closed",
            user_id=self.repo_card_one.assignees.first().id
        )
        pr_review_two_days_before_yesterday.save()

        self.assertIsNotNone(User.pr_reviews_done_in_past_seven_days)
        self.assertIsNotNone(User.total_pr_reviews_done_to_date)
        """