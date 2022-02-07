"""for each of the log entry creators in curriculum_tracking.activity_log_entry_creators, make sure it is called when it should be and creates the correct log entries
"""
from rest_framework.test import APITestCase

from test_mixins import APITestCaseMixin
from . import factories
from core.tests.factories import UserFactory
from curriculum_tracking.models import AgileCard, ContentItem
from activity_log.models import LogEntry
from curriculum_tracking import activity_log_entry_creators as creators
from curriculum_tracking.constants import COMPETENT


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
        self.login(actor_user)

        start_url = f"{self.get_instance_url(card.id)}start_project/"
        response = self.client.post(start_url)
        self.assertEqual(response.status_code, 200)

        card.refresh_from_db()

        # sanity check
        self.assertEqual(card.assignees.count(), 1)

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, actor_user)
        self.assertEqual(entry.effected_user, card.assignees.first())
        self.assertEqual(entry.object_1, card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_STARTED)

    # def test_start_topic(self):
    # TODO


# class log_card_stopped_Tests(TestCase):


# class log_card_review_requested_Tests(TestCase):
# every time a person moves a card into the review request column, we make an activity log entry


# class log_card_review_request_cancelled_Tests(TestCase):


# class log_card_moved_to_complete_Tests(TestCase):


# class log_card_moved_to_review_feedback_Tests(TestCase):


# class log_topic_competence_review_done_Tests(TestCase):


class log_project_competence_review_done_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def test_add_review(self):
        actor_user = UserFactory(is_superuser=True)
        card = factories.AgileCardFactory(
            status=AgileCard.IN_REVIEW,
            # recruit_project=None,
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        self.login(actor_user)

        start_url = f"{self.get_instance_url(card.id)}add_review/"
        response = self.client.post(
            start_url, data={"status": COMPETENT, "comments": "weee"}
        )
        self.assertEqual(response.status_code, 200)

        card.refresh_from_db()

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, actor_user)
        self.assertEqual(entry.effected_user, card.assignees.first())
        self.assertEqual(entry.event_type.name, creators.COMPETENCE_REVIEW_DONE)

        self.assertEqual(entry.object_1, card.recruit_project.project_reviews.first())
        self.assertEqual(entry.object_2, card.recruit_project)

        response = self.client.post(
            start_url, data={"status": COMPETENT, "comments": "blah more stuff"}
        )
        self.assertEqual(LogEntry.objects.count(), 2)


class log_card_review_requested_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def test_review_requested_authorised_user(self):
        actor_user = UserFactory(is_superuser=True, is_staff=True)
        content_item = factories.ProjectContentItemFactory(
            project_submission_type=ContentItem.LINK, template_repo=None
        )
        card = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=factories.RecruitProjectFactory(content_item=content_item),
            content_item=content_item,
        )
        self.login(actor_user)
        card.start_project()
        self.assertEqual(card.status, AgileCard.IN_PROGRESS)

        request_review_url = f"{self.get_instance_url(card.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 200)

        card.refresh_from_db()
        self.assertEqual(card.status, AgileCard.IN_REVIEW)

        # sanity check
        self.assertEqual(card.assignees.count(), 1)

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, actor_user)
        self.assertEqual(entry.effected_user, card.assignees.first())
        self.assertEqual(entry.object_1, card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_REVIEW_REQUESTED)

    def test_review_requested_assignee(self):

        content_item = factories.ProjectContentItemFactory(
            project_submission_type=ContentItem.LINK, template_repo=None
        )
        card = factories.AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=factories.RecruitProjectFactory(content_item=content_item),
            content_item=content_item,
        )
        self.login(card.assignees.first())
        card.start_project()
        self.assertEqual(card.status, AgileCard.IN_PROGRESS)

        request_review_url = f"{self.get_instance_url(card.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 200)

        card.refresh_from_db()
        self.assertEqual(card.status, AgileCard.IN_REVIEW)

        # sanity check
        self.assertEqual(card.assignees.count(), 1)

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, card.assignees.first())
        self.assertEqual(entry.effected_user, card.assignees.first())
        self.assertEqual(entry.object_1, card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_REVIEW_REQUESTED)

    def test_review_requested_non_authorised_user(self):
        actor_user = UserFactory(is_superuser=False)
        content_item = factories.ProjectContentItemFactory(
            project_submission_type=ContentItem.LINK, template_repo=None
        )
        card = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS,
            recruit_project=factories.RecruitProjectFactory(content_item=content_item),
            content_item=content_item,
        )
        self.login(actor_user)
        self.assertEqual(card.status, AgileCard.IN_PROGRESS)

        request_review_url = f"{self.get_instance_url(card.id)}request_review/"
        response = self.client.post(request_review_url)
        self.assertEqual(response.status_code, 403)
