from django.test import TestCase
from git_real.tests.factories import PullRequestFactory
from .factories import (
    RecruitProjectReviewFactory,
    TopicReviewFactory,
    UserFactory,
    AgileCardFactory,
    RecruitProjectFactory
)
import curriculum_tracking.activity_log_entry_creators as creators
from activity_log.models import LogEntry
from test_mixins import APITestCase, APITestCaseMixin
from core.tests import factories as core_factories
from datetime import timedelta
from django.utils import timezone
from curriculum_tracking.constants import (
    NOT_YET_COMPETENT,
)
from taggit.models import Tag


class log_project_competence_review_done_Tests(TestCase):
    def test_that_timestamp_properly_set(self):
        review = RecruitProjectReviewFactory()
        creators.log_project_competence_review_done(review)
        self.assertEqual(LogEntry.objects.first().timestamp, review.timestamp)

    def test_that_only_one_entry_created_for_one_review(self):
        self.assertEqual(LogEntry.objects.count(), 0)

        review1 = RecruitProjectReviewFactory()
        creators.log_project_competence_review_done(review1)
        creators.log_project_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 1)

        review2 = RecruitProjectReviewFactory()
        creators.log_project_competence_review_done(review2)
        creators.log_project_competence_review_done(review2)
        self.assertEqual(LogEntry.objects.count(), 2)

    def test_two_entries_created_for_two_reviews_with_second_done_within_debounce_period_by_another_user(self):
        review1 = RecruitProjectReviewFactory()
        review2 = RecruitProjectReviewFactory(
            status=review1.status,
            timestamp=review1.timestamp,
            comments=review1.comments,
            recruit_project=review1.recruit_project,
            reviewer_user=UserFactory()
        )
        creators.log_project_competence_review_done(review1)
        creators.log_project_competence_review_done(review2)
        self.assertEqual(LogEntry.objects.count(), 2)

    def test_logging_the_same_entry_twice_only_produces_one_log_entry(self):
        review1 = RecruitProjectReviewFactory()
        creators.log_project_competence_review_done(review1)
        creators.log_project_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 1)

    def test_log_project_creator_is_invoked_for_a_project_review_else_attribute_error_is_raised(self):
        review1 = RecruitProjectReviewFactory()
        with self.assertRaises(AttributeError) as exception:
            creators.log_topic_competence_review_done(review1)
        self.assertTrue(exception, AttributeError)
        self.assertEqual(LogEntry.objects.count(), 0)


class log_topic_competence_review_done_Tests(TestCase):
    def test_that_timestamp_properly_set(self):
        review = TopicReviewFactory()
        creators.log_topic_competence_review_done(review)
        self.assertEqual(LogEntry.objects.first().timestamp, review.timestamp)

    def test_that_only_one_entry_created_for_one_review(self):
        review1 = TopicReviewFactory()
        creators.log_topic_competence_review_done(review1)
        creators.log_topic_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 1)

        review2 = TopicReviewFactory()
        creators.log_topic_competence_review_done(review2)
        creators.log_topic_competence_review_done(review2)
        self.assertEqual(LogEntry.objects.count(), 2)

    def test_two_entries_created_for_two_reviews_with_second_done_within_debounce_period_by_another_user(self):
        review1 = TopicReviewFactory()
        review2 = TopicReviewFactory(
            status=review1.status,
            timestamp=review1.timestamp,
            comments=review1.comments,
            topic_progress=review1.topic_progress,
            reviewer_user=UserFactory()
        )

        creators.log_topic_competence_review_done(review1)
        creators.log_topic_competence_review_done(review2)
        self.assertEqual(LogEntry.objects.count(), 2)

    def test_logging_the_same_entry_twice_only_produces_one_log_entry(self):
        review1 = TopicReviewFactory()
        creators.log_topic_competence_review_done(review1)
        creators.log_topic_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 1)

    def test_log_topic_creator_is_invoked_for_a_topic_review_else_attribute_error_is_raised(self):
        review1 = TopicReviewFactory()
        with self.assertRaises(AttributeError) as exception:
            creators.log_project_competence_review_done(review1)
        self.assertTrue(exception, AttributeError)
        self.assertEqual(LogEntry.objects.count(), 0)


class log_project_and_topic_competence_reviews_done_TESTS(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = [
        "code_review_competent_since_last_review_request",
        "code_review_excellent_since_last_review_request",
        "code_review_red_flag_since_last_review_request",
        "code_review_ny_competent_since_last_review_request",
        "requires_cards",
        "required_by_cards",
        "project_submission_type_nice",
        "topic_needs_review",
        "topic_progress",
        "due_time",
        "complete_time",
        "review_request_time",
        "start_time",
        "tag_names",
        "can_start",
        "can_force_start",
    ]

    def verbose_instance_factory(self):
        project = RecruitProjectFactory()
        card = AgileCardFactory(recruit_project=project)
        card.reviewers.add(core_factories.UserFactory())
        card.assignees.add(core_factories.UserFactory())
        card.flavours.add(Tag.objects.create(name="asdsasa"))
        project.review_request_time = timezone.now() - timedelta(days=5)
        project.save()
        review = RecruitProjectReviewFactory(
            status=NOT_YET_COMPETENT,
            recruit_project=project,
        )
        review.timestamp = timezone.now() - timedelta(days=1)
        review.save()
        PullRequestFactory(repository=project.repository)
        return card

    def setUp(self):
        self.api_url = self.get_list_url()

    def test_log_project_competence_review_invoked_from_api_endpoint_for_project_review(self):
        super_user = UserFactory(is_superuser=True)
        review1 = RecruitProjectReviewFactory()
        self.login(super_user)
        breakpoint()
