from django.test import TestCase
from .factories import RecruitProjectReviewFactory, TopicReviewFactory
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
