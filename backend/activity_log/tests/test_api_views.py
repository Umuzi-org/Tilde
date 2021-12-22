from datetime import timedelta
from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from . import factories
from django.utils import timezone


class TestActivityLogDayCountViewset(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "activitylogdaycount-list"
    SUPPRESS_TEST_GET_LIST = True
    SUPPRESS_TEST_POST_TO_CREATE = True

    def setUp(self):
        self.today = timezone.now()

        self.yesterday = self.today - timedelta(days=1)

        self.entry1 = factories.LogEntryFactory()
        self.entry1.timestamp = self.today
        self.entry1.save()

        self.entry2 = factories.LogEntryFactory()
        self.entry2.timestamp = self.yesterday
        self.entry2.save()

        self.entry3 = factories.LogEntryFactory()
        self.entry3.timestamp = self.yesterday
        self.entry3.save()

        self.login_as_superuser()

    def test_list_api_count(self):
        url = self.get_list_url()

        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

        data_today = response.data[0]
        self.assertEqual(data_today["date"], str(self.today.date()))
        self.assertEqual(data_today["total"], 1)

        data_yesterday = response.data[1]
        self.assertEqual(data_yesterday["date"], str(self.yesterday.date()))
        self.assertEqual(data_yesterday["total"], 2)

    def test_list_api_filter_by_effected_user(self):
        url = f"{self.get_list_url()}?effected_user={self.entry1.effected_user.id}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["total"], 1)
        self.assertEqual(response.data[0]["date"], str(self.today.date()))

    def test_list_api_filter_by_event_type(self):
        url = f"{self.get_list_url()}?event_type__name={self.entry1.event_type.name}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["total"], 1)
        self.assertEqual(response.data[0]["date"], str(self.today.date()))
