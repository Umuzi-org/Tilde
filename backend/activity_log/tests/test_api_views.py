from datetime import timedelta
from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from . import factories
from django.utils import timezone
from curriculum_tracking.tests.factories import AgileCardFactory
from datetime import datetime


class TestActivityLogDayCountViewset(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "activitylogdaycount-list"
    SUPPRESS_TEST_GET_LIST = True
    SUPPRESS_TEST_POST_TO_CREATE = True

    def setUp(self):
        self.today = timezone.datetime(year=2022, month=10, day=3, hour=11, minute=1)

        self.yesterday = self.today - timedelta(days=1)

        self.entry_today_1 = factories.LogEntryFactory()
        self.entry_today_1.timestamp = self.today
        self.entry_today_1.save()

        self.entry_today_2 = factories.LogEntryFactory(
            event_type=self.entry_today_1.event_type,
            actor_user=self.entry_today_1.actor_user,
            effected_user=self.entry_today_1.effected_user,
        )
        self.entry_today_2.timestamp = self.today
        self.entry_today_2.save()
        assert self.entry_today_2.event_type == self.entry_today_1.event_type

        self.entry_yesterday_1 = factories.LogEntryFactory()
        self.entry_yesterday_1.timestamp = self.yesterday
        self.entry_yesterday_1.save()

        self.entry_yesterday_2 = factories.LogEntryFactory()
        self.entry_yesterday_2.timestamp = self.yesterday - timedelta(minutes=1)
        self.entry_yesterday_2.save()

        self.login_as_superuser()

    def test_list_api_count(self):
        url = self.get_list_url()

        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

        data_today = response.data[0]
        self.assertEqual(data_today["date"], str(self.today.date()))
        self.assertEqual(data_today["total"], 2)

        data_yesterday_1 = response.data[1]
        self.assertEqual(data_yesterday_1["date"], str(self.yesterday.date()))
        self.assertEqual(data_yesterday_1["total"], 1)

        data_yesterday_2 = response.data[2]
        self.assertEqual(data_yesterday_2["date"], str(self.yesterday.date()))
        self.assertEqual(data_yesterday_2["total"], 1)

    def test_list_api_filter_by_effected_user(self):
        url = (
            f"{self.get_list_url()}?effected_user={self.entry_today_1.effected_user.id}"
        )
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["total"], 2)
        self.assertEqual(response.data[0]["date"], str(self.today.date()))

    def test_list_api_filter_by_event_type(self):
        url = f"{self.get_list_url()}?event_type={self.entry_yesterday_1.event_type.id}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["total"], 1)
        self.assertEqual(response.data[0]["date"], str(self.yesterday.date()))

    def test_list_api_filter_by_timestamp_lte(self):
        url = f"{self.get_list_url()}?timestamp__lte={self.entry_yesterday_1.timestamp}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["total"], 1)

    def test_list_api_filter_by_timestamp_gte(self):
        url = f"{self.get_list_url()}?timestamp__gte={self.entry_today_1.timestamp}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["total"], 2)

    def test_list_api_filter_by_timestamp_lte_gte(self):
        url = f"{self.get_list_url()}?timestamp__lte={self.entry_today_2.timestamp}&timestamp__gte={self.entry_yesterday_2.timestamp}"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["total"], 2)


class TestEventTypeViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "eventtype-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        return factories.EventTypeFactory(description="a party")


class TestLogEntryViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "logentry-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        card = AgileCardFactory()
        log_entry = factories.LogEntryFactory()
        log_entry.object_1 = card
        log_entry.object_2 = card
        log_entry.save()
        return log_entry
