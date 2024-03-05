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

        self.do_login(self.user)

    def make_topic_card(self):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.IN_PROGRESS,
        )

        self.card.assignees.set([self.user])

    def test_stop_button_moves_topic_card_to_backlog_column(self):
        self.make_topic_card()

        self.page.click("text=Stop")

        self.page.wait_for_load_state("networkidle")

        backlog_column = self.page.text_content("div#column_RB")
        ip_column = self.page.text_content("div#column_IP")
        project_card_title = self.card.content_item.title

        self.assertNotIn(project_card_title, ip_column)
        self.assertIn(project_card_title, backlog_column)

    def test_topic_stop_button_logs_card_review_request_cancelled_event(
        self,
    ):
        self.make_topic_card()

        self.page.click("text=Stop")

        self.page.wait_for_load_state("networkidle")

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, self.user)
        self.assertEqual(entry.effected_user, self.card.assignees.first())
        self.assertEqual(entry.object_1, self.card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_REVIEW_REQUEST_CANCELLED)
