"""for each of the log entry creators in curriculum_tracking.activity_log_entry_creators, make sure it is called when it should be and creates the correct log entries
"""

from . import factories
from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
    RecruitProjectReview,
    TopicReview,
)
from curriculum_tracking.constants import NOT_YET_COMPETENT
from activity_log.models import LogEntry
from curriculum_tracking import activity_log_entry_creators as creators
from curriculum_tracking.constants import COMPETENT
from test_mixins import APITestCase, APITestCaseMixin
from .factories import (
    UserFactory,
    AgileCardFactory,
    RecruitProjectFactory,
)
from curriculum_tracking.tests.factories import (
    ProjectContentItemFactory,
    ContentItemFactory,
    TopicProgressFactory,
)
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

    def test_add_multiple_reviews(self):
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

        # two log entries will be created:
        # first log_project_competence_review_done
        # second log_card_moved_to_complete
        self.assertEqual(LogEntry.objects.count(), 2)
        entry = (
            LogEntry.objects.first()
        )  # meaning this is now actually the entry for log_card_moved_to_complete

        self.assertEqual(entry.actor_user, actor_user)
        self.assertEqual(entry.effected_user, card.assignees.first())
        self.assertEqual(entry.event_type.name, creators.COMPETENCE_REVIEW_DONE)

        self.assertEqual(entry.object_1, card.recruit_project.project_reviews.first())
        self.assertEqual(entry.object_2, card.recruit_project)

        response = self.client.post(
            start_url, data={"status": COMPETENT, "comments": "blah more stuff"}
        )
        # which means here there will now be 4 log entries in total
        self.assertEqual(LogEntry.objects.count(), 2)


class log_project_vs_topic_competence_reviews_done_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    @mock.patch(
        "curriculum_tracking.activity_log_entry_creators.log_topic_competence_review_done"
    )
    @mock.patch(
        "curriculum_tracking.activity_log_entry_creators.log_project_competence_review_done"
    )
    def test_log_project_competence_review_envoked_for_project_review(
        self, log_project_competence_review_done, log_topic_competence_review_done
    ):

        super_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(content_item=ProjectContentItemFactory())
        self.login(super_user)
        response = self.client.post(
            path=f"{self.get_instance_url(pk=card.id)}add_review/",
            data={"status": NOT_YET_COMPETENT, "comments": "dammit"},
        )
        self.assertTrue(response.status_code, 200)
        project_review = RecruitProjectReview.objects.first()
        log_project_competence_review_done.assert_called_with(project_review)
        log_topic_competence_review_done.assert_not_called()

    @mock.patch(
        "curriculum_tracking.activity_log_entry_creators.log_topic_competence_review_done"
    )
    @mock.patch(
        "curriculum_tracking.activity_log_entry_creators.log_project_competence_review_done"
    )
    def test_log_topic_competence_review_envoked_for_topic_review(
        self, log_project_competence_review_done, log_topic_competence_review_done
    ):
        super_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(content_item=ContentItemFactory())
        card.topic_progress = TopicProgressFactory()
        card.save()
        self.login(super_user)
        response = self.client.post(
            path=f"{self.get_instance_url(pk=card.id)}add_review/",
            data={"status": NOT_YET_COMPETENT, "comments": "dammit"},
        )
        topic_review = TopicReview.objects.first()
        self.assertTrue(response.status_code, 200)
        log_topic_competence_review_done.assert_called_with(topic_review)
        log_project_competence_review_done.assert_not_called()

    def test_log_project_competence_review_envoked_creates_log_entries(self):

        super_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(content_item=ProjectContentItemFactory())
        self.login(super_user)
        response = self.client.post(
            path=f"{self.get_instance_url(pk=card.id)}add_review/",
            data={"status": NOT_YET_COMPETENT, "comments": "dammit"},
        )
        self.assertTrue(response.status_code, 200)
        project_review = RecruitProjectReview.objects.first()
        log_entry = LogEntry.objects.first()
        self.assertEqual(log_entry.actor_user, project_review.reviewer_user)
        self.assertEqual(log_entry.timestamp, project_review.timestamp)

    def test_log_topic_competence_review_envoked_creates_log_entries(self):

        super_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(content_item=ContentItemFactory())
        card.topic_progress = TopicProgressFactory()
        card.save()
        self.login(super_user)
        response = self.client.post(
            path=f"{self.get_instance_url(pk=card.id)}add_review/",
            data={"status": NOT_YET_COMPETENT, "comments": "dammit"},
        )
        self.assertTrue(response.status_code, 200)
        topic_review = TopicReview.objects.first()
        log_entry = LogEntry.objects.first()
        self.assertEqual(log_entry.actor_user, topic_review.reviewer_user)
        self.assertEqual(log_entry.timestamp, topic_review.timestamp)


class log_card_review_requested_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def test_review_requested(self):
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


class log_card_review_feedback_correctly_called_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    @mock.patch(
        "curriculum_tracking.activity_log_entry_creators.log_card_moved_to_review_feedback"
    )
    @mock.patch(
        "curriculum_tracking.activity_log_entry_creators.log_card_moved_to_complete"
    )
    def test_card_review_feedback_called(
        self, log_card_moved_to_review_feedback, log_card_moved_to_complete
    ):
        actor_user = UserFactory(is_superuser=True)
        card = factories.AgileCardFactory(
            status=AgileCard.IN_REVIEW,
            content_item=factories.ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        self.login(actor_user)

        add_review_url = f"{self.get_instance_url(card.id)}add_review/"
        response = self.client.post(
            add_review_url, data={"status": NOT_YET_COMPETENT, "comments": "so sad"}
        )
        self.assertEqual(response.status_code, 200)

        card.refresh_from_db()
        project_review = RecruitProjectReview.objects.first()
        log_card_moved_to_review_feedback.assert_called_with(project_review)
        log_card_moved_to_complete.assert_not_called()
