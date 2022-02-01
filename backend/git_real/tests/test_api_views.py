from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from .factories import RepositoryFactory
from core.tests.factories import UserFactory
from .utils import get_body_and_headers
from django.urls import reverse
from django.utils import timezone
import dateutil.parser
import mock

from git_real import views
from git_real.models import Push
from git_real.permissions import IsWebhookSignatureOk
from git_real.helpers import github_timestamp_int_to_tz_aware_datetime


class RepositoryViewsetTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "repository-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        return RepositoryFactory(archived=True)


class PushEventTests(APITestCase):
    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_push_event_is_retrieved_from_api_end_point(self, has_permission):
        has_permission.return_value = True
        url = reverse(views.github_webhook)
        body, headers = get_body_and_headers("push")
        repo = RepositoryFactory(full_name=body["repository"]["full_name"])

        repository = body["repository"]
        head_commit = body["head_commit"]
        author_github_name = head_commit["author"]["username"]
        committer_github_name = head_commit["committer"]["username"]
        pusher_username = body["pusher"]["name"]
        message = head_commit["message"]
        head_commit_url = head_commit["url"]
        commit_timestamp = dateutil.parser.isoparse(head_commit["timestamp"])
        ref = body["ref"]
        pushed_at_time = github_timestamp_int_to_tz_aware_datetime(
            int(repository["pushed_at"])
        )

        # push_object = Push.create_or_update_from_github_api_data(repo, body)
        self.client.post(url, format="json", data=body, extra=headers)
        self.assertEqual(Push.objects.count(), 1)

        push = Push.objects.first()
        self.assertEqual(push.repository, repo)
        self.assertEqual(push.head_commit_url, head_commit_url)
        self.assertEqual(push.author_github_name, author_github_name)
        self.assertEqual(push.committer_github_name, committer_github_name)
        self.assertEqual(push.pusher_username, pusher_username)
        self.assertEqual(push.message, message)
        self.assertEqual(push.commit_timestamp, commit_timestamp)
        self.assertEqual(push.pushed_at_time, pushed_at_time)
        self.assertEqual(push.ref, ref)


    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def test_push_event_without_permission(self, has_permission):
        has_permission.return_value = False
        body, headers = get_body_and_headers("push")
        url = reverse(views.github_webhook)
        response = self.client.post(url, format="json", data=body, extra=headers)
        self.assertEqual(Push.objects.count(), 0)
