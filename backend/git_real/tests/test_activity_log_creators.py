"""for each of the log entry creators in git_real.activity_log_entry_creators, make sure it is called when it should be and creates the correct log entries
"""

from datetime import timedelta
from django.test import TestCase
from .factories import PullRequestReviewFactory, RepositoryFactory, PullRequestReview, PushFactory, Push, PullRequest,PullRequestFactory
import git_real.activity_log_creators as creators
from activity_log.models import LogEntry

from rest_framework.test import APITestCase

from git_real.models import Repository
from .utils import get_body_and_headers
from git_real.permissions import IsWebhookSignatureOk
from django.urls import reverse
from git_real import views
import mock

# from git_real.models import PullRequest, PullRequestReview, Push
from social_auth.tests.factories import SocialProfileFactory

class log_pr_opened_Tests(APITestCase):

    def test_that_timestamp_properly_set(self):
        pull_request = PullRequestFactory()
        creators.log_pr_opened(pull_request)
        self.assertAlmostEqual(LogEntry.objects.first().timestamp, pull_request.created_at,delta=timedelta(seconds=1))

    


class log_pr_reviewed_created_Tests(TestCase):
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


class log_pr_reviewed_Tests(APITestCase):
    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_adding_a_pr_review(self, has_permission):
        has_permission.return_value = True

        # self.assertEqual(PullRequest.objects.all().count(), 0)
        self.assertEqual(PullRequestReview.objects.all().count(), 0)

        body, headers = get_body_and_headers("pull_request_review_submitted")
        review_data = body["review"]
        social_profile = SocialProfileFactory(github_name=review_data["user"]["login"])

        url = reverse(views.github_webhook)

        repo = RepositoryFactory(full_name=body["repository"]["full_name"])

        self.client.post(url, format="json", data=body, extra=headers)

        # self.assertEqual(PullRequest.objects.all().count(), 1)
        self.assertEqual(PullRequestReview.objects.all().count(), 1)

        # pr = PullRequest.objects.first()
        pr_review = PullRequestReview.objects.first()

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, social_profile.user)
        self.assertEqual(entry.effected_user, repo.user)
        self.assertEqual(entry.object_1, pr_review)
        self.assertEqual(entry.object_2, repo)
        self.assertEqual(entry.event_type.name, creators.PR_REVIEWED)


class log_push_event_Tests(APITestCase):
    def test_that_timestamp_properly_set(self):
        push = PushFactory()
        creators.log_push_event(push)
        self.assertEqual(LogEntry.objects.first().timestamp, push.pushed_at_time)

    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_pushing(self, has_permission):
        has_permission.return_value = True

        self.assertEqual(Push.objects.all().count(), 0)   

        url = reverse(views.github_webhook)  

        body, headers = get_body_and_headers("push")
        RepositoryFactory(full_name=body["repository"]["full_name"])

        self.client.post(url, format="json", data=body, extra=headers)

        self.assertEqual(Push.objects.all().count(), 1)

        push = Push.objects.first()

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.effected_user, push.repository.user)
        self.assertEqual(entry.object_1, push)
        self.assertEqual(entry.object_2, push.repository)
        self.assertEqual(entry.event_type.name, creators.GIT_PUSH)