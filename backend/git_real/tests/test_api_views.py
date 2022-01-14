from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from git_real.permissions import IsWebhookSignatureOk
from git_real.models import Push
from .utils import get_body_and_headers
from .factories import RepositoryFactory
import mock
from . import factories
from django.urls import reverse
from git_real import views
import dateutil.parser
from git_real.helpers import (
    github_timestamp_int_to_tz_aware_datetime,
)
from core.tests.factories import UserFactory


class PushEventsFromRepositoriesViewsetTests(APITestCase, APITestCaseMixin):

    LIST_URL_NAME = "push-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        return factories.RepositoryFactory(archived=True)

    @mock.patch.object(IsWebhookSignatureOk, "has_permission")
    def setUp(self, has_permission):

        has_permission.return_value = True

        self.url = reverse(views.github_webhook)
        self.body, self.headers = get_body_and_headers("push")
        self.repo = RepositoryFactory(full_name=self.body["repository"]["full_name"])
        self.head_commit = self.body["head_commit"]
        self.author_github_name = self.head_commit["author"]["username"]
        self.committer_github_name = self.head_commit["committer"]["username"]
        self.message = self.head_commit["message"]
        self.head_commit_url = self.head_commit["url"]
        self.commit_timestamp = dateutil.parser.isoparse(self.head_commit["timestamp"])
        self.pusher_username = self.body["pusher"]["name"]
        self.repository = self.body["repository"]
        self.ref = self.body["ref"]
        self.pushed_at_time = github_timestamp_int_to_tz_aware_datetime(int(self.repository["pushed_at"]))

        self.client.post(self.url, format="json", data=self.body, extra=self.headers)

    def test_push_event_is_retrieved_from_api_end_point(self):

        recruit = UserFactory(is_superuser=True)
        self.assertEqual(Push.objects.count(), 1)
        self.login(recruit)
        url = self.get_list_url()
        ssh_url = self.repository.get('ssh_url')
        response = self.client.post(path=url, data={'repository': ssh_url})
        print(response)    # The response code should be 200

        """
        If you want to you can put a breakpoint() inside your view so that you can see that the post request is
        entering the correct view (It is, I am just mentioning it to you).  The only problem that you have
        has to do with your permission classes, this tests logs in as a super_user but still the response code is
        403 which means the request was understood but it was forbidden.
        """
