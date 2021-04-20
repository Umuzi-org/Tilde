from rest_framework.test import APITestCase
from pathlib import Path
import json
from django.urls import reverse
from git_real import views

# from django.test import Client
# from rest_framework.test import APIClient
from git_real.models import PullRequest
from git_real.helpers import strp_github_standard_time
from .factories import RepositoryFactory

import mock
from git_real.permissions import IsWebhookSignatureOk


def get_asset(name):
    path = Path(__file__).parent / "assets" / f"{name}.json"
    with open(path, "r") as f:
        return json.load(f)


def get_body_and_headers(asset_name):
    headers = get_asset(f"{asset_name}_request_headers")

    body = get_asset(f"{asset_name}_request_body")
    body["headers"] = headers

    return body, headers


class TestPullRequestOpened(APITestCase):
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
