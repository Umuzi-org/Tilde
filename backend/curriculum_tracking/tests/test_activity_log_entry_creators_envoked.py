"""for each of the log entry creators in curriculum_tracking.activity_log_entry_creators, make sure it is called when it should be and creates the correct log entries
"""
from rest_framework.test import APITestCase
from django.test import TestCase
import curriculum_tracking
from test_mixins import APITestCaseMixin
from . import factories
from core.tests.factories import UserFactory
from .factories import AgileCardFactory, RecruitProjectFactory, ProjectContentItemFactory
from curriculum_tracking.models import AgileCard, ContentItem
from activity_log.models import LogEntry
from curriculum_tracking import activity_log_entry_creators as creators
from curriculum_tracking import activity_log_entry_creators
from curriculum_tracking.constants import COMPETENT
from django.utils import timezone
from mock import patch
import datetime
import pytz
import mock


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
        assert response.status_code == 200, response.data

        card.refresh_from_db()

        # sanity check
        assert card.assignees.count() == 1

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


class log_card_moved_to_complete_Tests(TestCase):

    def test_card_to_complete_creates_one_log_entry(self):

        actor_user = UserFactory(is_superuser=True)
        card = factories.AgileCardFactory(
            status=AgileCard.COMPLETE,
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        card.save()

        creators.log_card_moved_to_complete(card, actor_user)
        self.assertTrue(card.status==AgileCard.COMPLETE)
        self.assertEqual(LogEntry.objects.count(), 1)
        self.assertEqual(LogEntry.objects.first().actor_user, actor_user)

    def test_card_to_complete_then_rf_then_complete_creates_one_complete_entry_within_debounce_period(self):
        """
        Although two LogEntries are created, only one of them is of status 'CARD_MOVED_TO_COMPLETE'
        """
        actor_user = UserFactory(is_superuser=True)
        card = factories.AgileCardFactory(
            status=AgileCard.COMPLETE,
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )

        card.save()
        creators.log_card_moved_to_complete(card, actor_user)
        self.assertTrue(card.status == AgileCard.COMPLETE)
        self.assertEqual(LogEntry.objects.count(), 1)

        card.status = AgileCard.REVIEW_FEEDBACK
        card.save()
        creators.log_card_moved_to_review_feedback(card, actor_user)
        self.assertTrue(card.status == AgileCard.REVIEW_FEEDBACK)
        self.assertEqual(LogEntry.objects.count(), 2)

        card.status = AgileCard.COMPLETE
        card.save()
        creators.log_card_moved_to_complete(card, actor_user)
        self.assertTrue(card.status == AgileCard.COMPLETE)
        log_entries = [entry.event_type.name for entry in LogEntry.objects.all()].count('CARD_MOVED_TO_COMPLETE')
        self.assertTrue(log_entries, 1)

    @patch('django.utils.timezone.now',
           return_value=datetime.datetime(
            timezone.now().year,
            timezone.now().month,
            timezone.now().day,
            timezone.now().hour,
            timezone.now().minute,
            timezone.now().second,
            tzinfo=pytz.timezone('utc'))
    )
    def test_card_to_complete_then_rf_then_complete_creates_two_complete_entries_after_debounce_period(self, mock_now):

        actor_user = UserFactory(is_superuser=True)
        card = factories.AgileCardFactory(
            status=AgileCard.IN_REVIEW,
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )

        initial_complete_review = factories.RecruitProjectReviewFactory(
            recruit_project=card.recruit_project,
            timestamp=timezone.now(),
            reviewer_user=actor_user
        )
        card.status = AgileCard.COMPLETE
        card.save()
        creators.log_card_moved_to_complete(card, actor_user)
        self.assertTrue(card.status == AgileCard.COMPLETE)
        self.assertEqual(LogEntry.objects.count(), 1)

        nyc_review = factories.RecruitProjectReviewFactory(
            recruit_project=card.recruit_project,
            timestamp=initial_complete_review.timestamp + timezone.timedelta(seconds=20),
            reviewer_user=actor_user
        )
        card.status = AgileCard.REVIEW_FEEDBACK
        card.save()
        creators.log_card_moved_to_review_feedback(card, actor_user)

        complete_review = factories.RecruitProjectReviewFactory(
            recruit_project=card.recruit_project,
            timestamp=nyc_review.timestamp + timezone.timedelta(seconds=120),
            reviewer_user=actor_user
        )
        card.status = AgileCard.COMPLETE
        card.save()

        mock_now.return_value = timezone.now() + timezone.timedelta(seconds=121)
        creators.log_card_moved_to_complete(card, actor_user)
        self.assertTrue(card.status == AgileCard.COMPLETE)

        log_entries = [entry.event_type.name for entry in LogEntry.objects.all()].count('CARD_MOVED_TO_COMPLETE')
        self.assertTrue(log_entries, 3)


class log_card_moved_to_complete_api_view_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    FIELDS_THAT_CAN_BE_FALSEY = [
        "code_review_competent_since_last_review_request",
        "code_review_excellent_since_last_review_request",
        "code_review_red_flag_since_last_review_request",
        "code_review_ny_competent_since_last_review_request",
        "requires_cards",
        "required_by_cards",
        "project_submission_type_nice",
        "topic_needs_review",
        "topic_progress",
        "due_time",
        "complete_time",
        "review_request_time",
        "start_time",
        "tag_names",
        "can_start",
        "can_force_start",
        "flavour_names",
        "open_pr_count",
        "oldest_open_pr_updated_time",
        "users_that_reviewed_since_last_review_request"
    ]

    def verbose_instance_factory(self):
        project = RecruitProjectFactory()
        card = AgileCardFactory(recruit_project=project)
        return card

    def setUp(self):
        self.api_url = self.get_list_url()

    @mock.patch.object(curriculum_tracking.activity_log_entry_creators, 'log_card_moved_to_complete')
    @mock.patch.object(curriculum_tracking.activity_log_entry_creators, 'log_topic_competence_review_done')
    @mock.patch.object(curriculum_tracking.activity_log_entry_creators, 'log_project_competence_review_done')
    def test_log_project_competence_review_invoked_from_api_endpoint_for_project_review(
            self, log_project_competence_review_done, log_topic_competence_review_done, log_card_moved_to_complete
    ):
        super_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(content_item=ProjectContentItemFactory())
        self.login(super_user)
        response = self.client.post(
            path=f'{self.api_url}{card.id}/add_review/',
            data={"status": "NYC", "comments": "dammit"}
        )

        self.assertTrue(response.status_code, 200)
        log_project_competence_review_done.assert_called()
        log_topic_competence_review_done.assert_not_called()
        log_card_moved_to_complete.assert_not_called()

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
        assert response.status_code == 200, response.data

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
