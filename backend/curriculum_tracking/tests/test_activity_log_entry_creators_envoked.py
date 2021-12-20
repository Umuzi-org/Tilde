"""for each of the log entry creators in curriculum_tracking.activity_log_entry_creators, make sure it is called when it should be and creates the correct log entries
"""
# from django.test import TestCase
from rest_framework.test import APITestCase

from test_mixins import APITestCaseMixin
from . import factories
from core.tests.factories import UserFactory
from curriculum_tracking.models import AgileCard, ContentItem
from activity_log.models import LogEntry
from curriculum_tracking import activity_log_entry_creators as creators


class log_card_started_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def test_start_project(self):
        actor_user = UserFactory(is_superuser=True)
        card = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=None,
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        start_url = f"{self.get_instance_url(card.id)}start_project/"
        self.login(actor_user)

        response = self.client.post(start_url)

        card.refresh_from_db()

        # sanity check
        assert card.assignees.count() == 1
        assert response.status_code == 200

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, actor_user)
        self.assertEqual(entry.effected_user, card.assignees.first())
        self.assertEqual(entry.object_1, card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_STARTED)

    # def test_start_topic(self):


# class log_card_stopped_Tests(TestCase):


# class log_card_review_requested_Tests(TestCase):
# every time a person moves a card into the review request column, we make an activity log entry


# class log_card_review_request_cancelled_Tests(TestCase):


# class log_card_moved_to_complete_Tests(TestCase):


# class log_card_moved_to_review_feedback_Tests(TestCase):


# class log_project_competence_review_done_Tests(TestCase):


# class log_topic_competence_review_done_Tests(TestCase):
