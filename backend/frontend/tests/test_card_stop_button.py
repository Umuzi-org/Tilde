from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
)
from curriculum_tracking.models import ContentItem, AgileCard
from .frontend_test_mixin import FrontendTestMixin
from activity_log.models import LogEntry
import curriculum_tracking.activity_log_entry_creators as creators


class TestCardStopButton(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()
        

    def make_topic_card(self):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )

        self.card.assignees.set([self.user])

        self.card.start_topic()

    def make_project_card(self, project_submission_type):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=project_submission_type,
            ),
            status=AgileCard.IN_PROGRESS,
        )
        self.card.assignees.set([self.user])

    def test_topic_stop_button_logs_card_stopped_event(
        self,
    ):
        self.make_topic_card()

        self.do_login(self.user)
        self.page.wait_for_load_state()

        self.page.locator("text=Stop").click()
        self.page.wait_for_load_state("networkidle")

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, self.user)
        self.assertEqual(entry.effected_user, self.card.assignees.first())
        self.assertEqual(entry.object_1, self.card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_STOPPED)

    def test_project_stop_button_logs_card_stopped_event(
        self,
    ):
        self.make_project_card(ContentItem.LINK)

        self.do_login(self.user)
        self.page.wait_for_load_state()

        self.page.locator("text=Stop").click()
        self.page.wait_for_load_state("networkidle")

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, self.user)
        self.assertEqual(entry.effected_user, self.card.assignees.first())
        self.assertEqual(entry.object_1, self.card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_STOPPED)
