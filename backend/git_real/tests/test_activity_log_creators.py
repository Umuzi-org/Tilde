from django.test import TestCase
from .factories import PullRequestReviewFactory, PullRequestFactory,UserFactory
import git_real.activity_log_creators as creators
from activity_log.models import LogEntry


class log_pr_reviewed_Tests(TestCase):
    def test_that_timestamp_properly_set(self):
        review = PullRequestReviewFactory()
        creators.log_pr_reviewed(review)
        self.assertEqual(LogEntry.objects.first().timestamp, review.submitted_at)

    def test_that_only_one_entry_created_for_one_review(self):
        self.assertEqual(LogEntry.objects.count(), 0)

        review1 = PullRequestReviewFactory()
        creators.log_pr_reviewed(review1)
        creators.log_pr_reviewed(review1)
        self.assertEqual(LogEntry.objects.count(), 1)

        review2 = PullRequestReviewFactory()
        creators.log_pr_reviewed(review2)
        creators.log_pr_reviewed(review2)
        self.assertEqual(LogEntry.objects.count(), 2)

