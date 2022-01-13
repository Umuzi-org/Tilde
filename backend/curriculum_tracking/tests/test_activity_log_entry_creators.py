from django.test import TestCase
from .factories import RecruitProjectReviewFactory, TopicReviewFactory, UserFactory
import curriculum_tracking.activity_log_entry_creators as creators
from activity_log.models import LogEntry


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

    def test_log_project_creator_is_invoked_for_a_project_review(self):
        review1 = RecruitProjectReviewFactory()
        try:
            creators.log_topic_competence_review_done(review1)
        except AttributeError as error:
            self.assertTrue(error)
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

    def test_log_topic_creator_is_invoked_for_a_topic_review(self):
        review1 = TopicReviewFactory()
        try:
            creators.log_project_competence_review_done(review1)
        except AttributeError as error:
            self.assertTrue(error)
        self.assertEqual(LogEntry.objects.count(), 0)