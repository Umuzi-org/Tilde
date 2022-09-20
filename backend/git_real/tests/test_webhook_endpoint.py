from rest_framework.test import APITestCase
from django.urls import reverse
from git_real import views
from git_real.models import PullRequest, PullRequestReview, Push
from git_real.helpers import (
    strp_github_standard_time,
    github_timestamp_int_to_tz_aware_datetime,
)
from .factories import RepositoryFactory
from social_auth.tests.factories import SocialProfileFactory
import mock
from git_real.permissions import IsWebhookSignatureOk
from django.utils import timezone
import dateutil.parser
import git_real.activity_log_creators as creators
from activity_log.models import LogEntry

# from timezone_helpers import timestamp_zoned_str_to_tz_aware_datetime
from .utils import get_body_and_headers


class TestPullRequestEvents(APITestCase):
    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_that_opening_a_pr_creates_if_not_exists(self, has_permission):
        has_permission.return_value = True

        self.assertEqual(PullRequest.objects.all().count(), 0)

        body, headers = get_body_and_headers("pull_request_opened")
        url = reverse(views.github_webhook)

        repo = RepositoryFactory(full_name=body["repository"]["full_name"])

        self.client.post(url, format="json", data=body, extra=headers)

        self.assertEqual(PullRequest.objects.all().count(), 1)

        pr = PullRequest.objects.first()
        self.assertEqual(pr.repository.full_name, body["repository"]["full_name"])
        self.assertEqual(pr.repository, repo)
        self.assertEqual(pr.state, body["pull_request"]["state"])
        self.assertEqual(pr.title, body["pull_request"]["title"])
        self.assertEqual(pr.body, body["pull_request"]["body"])
        self.assertEqual(
            pr.created_at, strp_github_standard_time(body["pull_request"]["created_at"])
        )
        self.assertEqual(
            pr.updated_at, strp_github_standard_time(body["pull_request"]["updated_at"])
        )
        self.assertEqual(
            pr.closed_at, strp_github_standard_time(body["pull_request"]["closed_at"])
        )
        self.assertEqual(
            pr.merged_at, strp_github_standard_time(body["pull_request"]["merged_at"])
        )
        self.assertEqual(pr.number, body["pull_request"]["number"])

        self.client.post(url, format="json", data=body, extra=headers)
        self.assertEqual(PullRequest.objects.all().count(), 1)

    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_pull_request_closed_closes_it_if_it_exists(self, has_permission):
        has_permission.return_value = True

        body, headers = get_body_and_headers("pull_request_closed")
        url = reverse(views.github_webhook)

        repo = RepositoryFactory(full_name=body["repository"]["full_name"])

        self.client.post(url, format="json", data=body, extra=headers)

        self.assertEqual(PullRequest.objects.all().count(), 1)


class TestPullRequestReview(APITestCase):
    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_that_pr_review_event_creates_a_pr_review_object(self, has_permission):
        has_permission.return_value = True

        self.assertEqual(PullRequest.objects.all().count(), 0)
        self.assertEqual(PullRequestReview.objects.all().count(), 0)

        body, headers = get_body_and_headers("pull_request_review_submitted")
        review_data = body["review"]
        social_profile = SocialProfileFactory(github_name=review_data["user"]["login"])

        url = reverse(views.github_webhook)

        repo = RepositoryFactory(full_name=body["repository"]["full_name"])

        self.client.post(url, format="json", data=body, extra=headers)

        self.assertEqual(PullRequest.objects.all().count(), 1)
        self.assertEqual(PullRequestReview.objects.all().count(), 1)

        pr = PullRequest.objects.first()
        review = PullRequestReview.objects.first()

        self.assertEqual(review.html_url, review_data["html_url"])
        self.assertEqual(review.pull_request, pr)
        self.assertEqual(review.author_github_name, social_profile.github_name)
        self.assertEqual(review.body, review_data["body"])
        self.assertEqual(review.commit_id, review_data["commit_id"])
        self.assertEqual(review.state, review_data["state"])
        self.assertEqual(review.user, social_profile.user)

        self.assertEqual(
            review.submitted_at, strp_github_standard_time(review_data["submitted_at"])
        )

        self.client.post(url, format="json", data=body, extra=headers)
        self.assertEqual(PullRequest.objects.all().count(), 1)
        self.assertEqual(PullRequestReview.objects.all().count(), 1)

    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_that_pr_review_event_doesnt_duplicate_pr_review_object(
        self, has_permission
    ):
        has_permission.return_value = True

        self.assertEqual(PullRequest.objects.all().count(), 0)
        self.assertEqual(PullRequestReview.objects.all().count(), 0)

        body, headers = get_body_and_headers("pull_request_review_submitted")
        review_data = body["review"]
        social_profile = SocialProfileFactory(github_name=review_data["user"]["login"])

        url = reverse(views.github_webhook)

        repo = RepositoryFactory(full_name=body["repository"]["full_name"])

        self.client.post(url, format="json", data=body, extra=headers)

        self.assertEqual(PullRequest.objects.all().count(), 1)
        self.assertEqual(PullRequestReview.objects.all().count(), 1)

        # mess up all the fields except html_url
        review = PullRequestReview.objects.first()
        review.author_github_name = ""
        review.submitted_at = timezone.now()
        review.body = ""
        review.commit_id = ""
        review.state = ""
        review.user = None
        review.save()

        self.client.post(url, format="json", data=body, extra=headers)

        pr = PullRequest.objects.first()
        review = PullRequestReview.objects.first()

        self.assertEqual(review.html_url, review_data["html_url"])
        self.assertEqual(review.pull_request, pr)
        self.assertEqual(review.author_github_name, social_profile.github_name)
        self.assertEqual(review.body, review_data["body"])
        self.assertEqual(review.commit_id, review_data["commit_id"])
        self.assertEqual(review.state, review_data["state"])
        self.assertEqual(review.user, social_profile.user)

        self.assertEqual(
            review.submitted_at, strp_github_standard_time(review_data["submitted_at"])
        )

        self.client.post(url, format="json", data=body, extra=headers)
        self.assertEqual(PullRequest.objects.all().count(), 1)
        self.assertEqual(PullRequestReview.objects.all().count(), 1)


class PushEventTests(APITestCase):
    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_that_push_event_saves(self, has_permission):
        has_permission.return_value = True
        url = reverse(views.github_webhook)

        body, headers = get_body_and_headers("push")
        repo = RepositoryFactory(full_name=body["repository"]["full_name"])

        head_commit = body["head_commit"]
        author_github_name = head_commit["author"]["username"]
        committer_github_name = head_commit["committer"]["username"]
        message = head_commit["message"]
        head_commit_url = head_commit["url"]
        # commit_timestamp = timestamp_zoned_str_to_tz_aware_datetime(
        #     head_commit["timestamp"]
        # )

        commit_timestamp = dateutil.parser.isoparse(head_commit["timestamp"])

        pusher_username = body["pusher"]["name"]
        repository = body["repository"]
        ref = body["ref"]

        # repo_full_name = repository["full_name"]
        pushed_at_time = github_timestamp_int_to_tz_aware_datetime(
            int(repository["pushed_at"])
        )
        self.client.post(url, format="json", data=body, extra=headers)

        self.assertEqual(Push.objects.count(), 1)
        push = Push.objects.first()

        self.assertEqual(push.author_github_name, author_github_name)
        self.assertEqual(push.committer_github_name, committer_github_name)
        self.assertEqual(push.message, message)
        self.assertEqual(push.head_commit_url, head_commit_url)
        self.assertEqual(push.pusher_username, pusher_username)
        self.assertEqual(push.pushed_at_time, pushed_at_time)
        self.assertEqual(push.ref, ref)
        self.assertEqual(push.repository, repo)
        self.assertEqual(push.commit_timestamp, commit_timestamp)
        # self.assertEqual(push.commit_timestamp.isoformat(), commit_timestamp.isoformat())
        # BUG: if you uncomment the above line then you'll see that the stored timestamps aren't keeping the timezonne info. Please fix here and in all other places where we are getting info from gihub

        self.client.post(url, format="json", data=body, extra=headers)

        self.assertEqual(Push.objects.count(), 1)

        creators.log_push_event(push)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.event_type.name, creators.GIT_PUSH)


class TestNoHeadCommitInPushEvents(APITestCase):
    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_payload_without_head_commit_details_is_handled_but_not_stored_to_db(
        self, has_permission
    ):

        has_permission.return_value = True
        body, headers = get_body_and_headers("webhook_push")
        repo = RepositoryFactory(full_name=body["repository"]["full_name"])
        push_object = Push.create_or_update_from_github_api_data(repo, body)
        self.assertEqual(Push.objects.count(), 0)
