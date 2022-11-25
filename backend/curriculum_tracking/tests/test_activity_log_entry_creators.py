"""for each of the log entry creators in curriculum_tracking.activity_log_entry_creators, make sure it is called when it should be and creates the correct log entries
"""

from django.test import TestCase
from .factories import (
    RecruitProjectReviewFactory,
    TopicReviewFactory,
    UserFactory,
    AgileCardFactory,
    RecruitProjectFactory,
    ContentItemFactory,
)
import curriculum_tracking.activity_log_entry_creators as creators
from activity_log.models import EventType, LogEntry

from curriculum_tracking.models import (
    AgileCard,
    ContentItem,
    RecruitProjectReview,
    TopicReview,
)
from curriculum_tracking.constants import NOT_YET_COMPETENT
from curriculum_tracking.constants import COMPETENT
from test_mixins import APITestCase, APITestCaseMixin

from curriculum_tracking.tests.factories import (
    ProjectContentItemFactory,
    ContentItemFactory,
    TopicProgressFactory,
)
import mock
from django.utils import timezone


class log_project_competence_review_done_Tests(TestCase):
    def test_that_timestamp_properly_set(self):
        review = RecruitProjectReviewFactory()
        creators.log_project_competence_review_done(review)
        self.assertEqual(LogEntry.objects.first().timestamp, review.timestamp)

    def test_that_only_one_entry_created_for_one_review(self):
        self.assertEqual(LogEntry.objects.count(), 0)

        review1 = RecruitProjectReviewFactory()
        creators.log_project_competence_review_done(review1)
        creators.log_project_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 1)

        review2 = RecruitProjectReviewFactory()
        creators.log_project_competence_review_done(review2)
        creators.log_project_competence_review_done(review2)
        self.assertEqual(LogEntry.objects.count(), 2)

    def test_log_project_creator_is_invoked_for_a_project_review_else_attribute_error_is_raised(
        self,
    ):
        review1 = RecruitProjectReviewFactory()
        with self.assertRaises(AttributeError) as exception:
            creators.log_topic_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 0)


class log_topic_competence_review_done_Tests(TestCase):
    def test_that_timestamp_properly_set(self):
        review = TopicReviewFactory()
        creators.log_topic_competence_review_done(review)
        self.assertEqual(LogEntry.objects.first().timestamp, review.timestamp)

    def test_that_only_one_entry_created_for_one_review(self):
        review1 = TopicReviewFactory()
        creators.log_topic_competence_review_done(review1)
        creators.log_topic_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 1)

        review2 = TopicReviewFactory()
        creators.log_topic_competence_review_done(review2)
        creators.log_topic_competence_review_done(review2)
        self.assertEqual(LogEntry.objects.count(), 2)

    def test_two_entries_created_for_two_reviews_with_second_done_within_debounce_period_by_another_user(
        self,
    ):
        review1 = TopicReviewFactory()
        review2 = TopicReviewFactory(
            status=review1.status,
            timestamp=review1.timestamp,
            comments=review1.comments,
            topic_progress=review1.topic_progress,
            reviewer_user=UserFactory(),
        )

        creators.log_topic_competence_review_done(review1)
        creators.log_topic_competence_review_done(review2)
        self.assertEqual(LogEntry.objects.count(), 2)

    def test_logging_the_same_entry_twice_only_produces_one_log_entry(self):
        review1 = TopicReviewFactory()
        creators.log_topic_competence_review_done(review1)
        creators.log_topic_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 1)

    def test_log_topic_creator_is_invoked_for_a_topic_review_else_attribute_error_is_raised(
        self,
    ):
        review1 = TopicReviewFactory()
        with self.assertRaises(AttributeError) as exception:
            creators.log_project_competence_review_done(review1)
        self.assertEqual(LogEntry.objects.count(), 0)


class log_card_started_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def test_start_project(self):
        actor_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=None,
            content_item=ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        creators.EventType.objects.get_or_create(name=creators.CARD_MOVED_TO_REVIEW_FEEDBACK)
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


class log_card_moved_to_complete_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def test_card_moved_to_complete_called(self):
        actor_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(
            status=AgileCard.IN_REVIEW,
            content_item=ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        self.login(actor_user)

        creators.EventType.objects.get_or_create(name=creators.CARD_MOVED_TO_REVIEW_FEEDBACK)

        add_review_url = f"{self.get_instance_url(card.id)}add_review/"
        response = self.client.post(
            add_review_url, data={"status": COMPETENT, "comments": "woohoo"}
        )
        self.assertEqual(response.status_code, 200)

        entry = LogEntry.objects.last()

        card.refresh_from_db()
        self.assertEqual(card.status, AgileCard.COMPLETE)
        self.assertEqual(entry.event_type.name, creators.CARD_MOVED_TO_COMPLETE)
        self.assertEqual(LogEntry.objects.count(), 2)
        self.assertEqual(entry.effected_user, card.assignees.first())
        self.assertEqual(entry.actor_user, actor_user)
        self.assertEqual(entry.object_1, card.recruit_project)


# class log_card_moved_to_review_feedback_Tests(TestCase):


# class log_topic_competence_review_done_Tests(TestCase):


class log_multiple_project_competence_review_done_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def test_add_multiple_reviews(self):
        actor_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(
            status=AgileCard.IN_REVIEW,
            # recruit_project=None,
            content_item=ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        creators.EventType.objects.get_or_create(name=creators.CARD_MOVED_TO_REVIEW_FEEDBACK)
        project = card.recruit_project
        project.review_request_time = timezone.now() - timezone.timedelta(days=1)
        project.save()
        self.login(actor_user)

        add_review_url = f"{self.get_instance_url(card.id)}add_review/"
        response = self.client.post(
            add_review_url, data={"status": COMPETENT, "comments": "weee"}
        )
        self.assertEqual(response.status_code, 200)

        card.refresh_from_db()

        self.assertEqual(LogEntry.objects.count(), 2)

        competence_review_entry = LogEntry.objects.all()[0]
        card_to_complete_entry = LogEntry.objects.all()[1]

        self.assertEqual(competence_review_entry.actor_user, actor_user)
        self.assertEqual(competence_review_entry.effected_user, card.assignees.first())
        self.assertEqual(
            competence_review_entry.event_type.name, creators.COMPETENCE_REVIEW_DONE
        )
        self.assertEqual(
            competence_review_entry.object_1,
            card.recruit_project.project_reviews.first(),
        )
        self.assertEqual(competence_review_entry.object_2, card.recruit_project)

        self.assertEqual(card_to_complete_entry.actor_user, actor_user)
        self.assertEqual(card_to_complete_entry.effected_user, card.assignees.first())
        self.assertEqual(
            card_to_complete_entry.event_type.name, creators.CARD_MOVED_TO_COMPLETE
        )
        self.assertEqual(
            card_to_complete_entry.object_1,
            card.recruit_project,
        )
        self.assertEqual(card_to_complete_entry.object_2, None)

        response = self.client.post(
            add_review_url, data={"status": COMPETENT, "comments": "blah more stuff"}
        )
        card.refresh_from_db()

        self.assertEqual(LogEntry.objects.count(), 3)


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
    def test_log_project_competence_review_envoked(
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
    def test_log_topic_competence_review_envoked(
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


class log_card_review_requested_and_cancelled_Tests(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "agilecard-list"
    SUPPRESS_TEST_POST_TO_CREATE = True
    SUPPRESS_TEST_GET_LIST = True

    def setUp(self):
        self.actor_user = UserFactory(is_superuser=True, is_staff=True)
        self.content_item = ProjectContentItemFactory(
            project_submission_type=ContentItem.LINK, template_repo=None
        )
        self.card = AgileCardFactory(
            status=AgileCard.READY,
            recruit_project=RecruitProjectFactory(content_item=self.content_item),
            content_item=self.content_item,
        )
        creators.EventType.objects.get_or_create(name=creators.CARD_MOVED_TO_REVIEW_FEEDBACK)
        self.login(self.actor_user)
        self.card.start_project()
        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)

    def test_review_requested(self):

        request_review_url = f"{self.get_instance_url(self.card.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card.refresh_from_db()
        self.assertEqual(self.card.status, AgileCard.IN_REVIEW)

        # sanity check
        self.assertEqual(self.card.assignees.count(), 1)

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, self.actor_user)
        self.assertEqual(entry.effected_user, self.card.assignees.first())
        self.assertEqual(entry.object_1, self.card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_REVIEW_REQUESTED)

    def test_cancel_review_requested(self):

        request_review_url = f"{self.get_instance_url(self.card.id)}request_review/"
        response = self.client.post(request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card.refresh_from_db()
        self.assertEqual(self.card.status, AgileCard.IN_REVIEW)

        cancel_request_review_url = (
            f"{self.get_instance_url(self.card.id)}cancel_review_request/"
        )
        response = self.client.post(cancel_request_review_url)

        self.assertEqual(response.status_code, 200)

        self.card.refresh_from_db()
        self.assertEqual(self.card.status, AgileCard.IN_PROGRESS)

        self.assertEqual(LogEntry.objects.count(), 2)
        entry = LogEntry.objects.last()

        self.assertEqual(entry.actor_user, self.actor_user)
        self.assertEqual(entry.effected_user, self.card.assignees.first())
        self.assertEqual(entry.object_1, self.card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_REVIEW_REQUEST_CANCELLED)


class log_card_review_feedback_vs_log_card_move_to_complete_called_Tests(
    APITestCase, APITestCaseMixin
):
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
        self, log_card_moved_to_complete, log_card_moved_to_review_feedback
    ):
        actor_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(
            status=AgileCard.IN_REVIEW,
            content_item=ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        self.login(actor_user)
        creators.EventType.objects.get_or_create(name=creators.CARD_MOVED_TO_REVIEW_FEEDBACK)

        add_review_url = f"{self.get_instance_url(card.id)}add_review/"
        response = self.client.post(
            add_review_url, data={"status": NOT_YET_COMPETENT, "comments": "so sad"}
        )
        self.assertEqual(response.status_code, 200)


        card.refresh_from_db()
        self.assertEqual(card.status, AgileCard.REVIEW_FEEDBACK)
        log_card_moved_to_review_feedback.assert_called_with(card, actor_user)
        log_card_moved_to_complete.assert_not_called()

    @mock.patch(
        "curriculum_tracking.activity_log_entry_creators.log_card_moved_to_review_feedback"
    )
    @mock.patch(
        "curriculum_tracking.activity_log_entry_creators.log_card_moved_to_complete"
    )
    def test_card_moved_to_complete_called(
        self, log_card_moved_to_complete, log_card_moved_to_review_feedback
    ):
        actor_user = UserFactory(is_superuser=True)
        card = AgileCardFactory(
            status=AgileCard.IN_REVIEW,
            content_item=ProjectContentItemFactory(
                project_submission_type=ContentItem.LINK, template_repo=None
            ),
        )
        self.login(actor_user)
        creators.EventType.objects.get_or_create(name=creators.CARD_MOVED_TO_REVIEW_FEEDBACK)

        add_review_url = f"{self.get_instance_url(card.id)}add_review/"
        response = self.client.post(
            add_review_url, data={"status": COMPETENT, "comments": "woohoo"}
        )
        self.assertEqual(response.status_code, 200)

        card.refresh_from_db()
        self.assertEqual(card.status, AgileCard.COMPLETE)
        log_card_moved_to_complete.assert_called_with(card, actor_user)
        log_card_moved_to_review_feedback.assert_not_called()
