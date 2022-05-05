from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from .factories import RepositoryFactory, PushFactory
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


class PushEventTests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "push-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        return PushFactory()
