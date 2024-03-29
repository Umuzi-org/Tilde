from activity_log.models import LogEntry
from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory, ContentItemFactory
from curriculum_tracking.models import ContentItem, AgileCard
import curriculum_tracking.activity_log_entry_creators as creators
from .frontend_test_mixin import FrontendTestMixin


class TestCardDoneButton(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()

        self.do_login(self.user)

    
    def make_topic_card(self):
        self.card: AgileCard = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.TOPIC,
            ),
            status=AgileCard.READY,
        )
        self.card.assignees.set([self.user])
        self.card.start_topic()
    
    def make_project_card(self):
        self.card: AgileCard = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.IN_PROGRESS,
        )
        self.card.assignees.set([self.user])

    def make_outstanding_ir_project_card(self):
        self.card: AgileCard = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.IN_REVIEW,
        )
        self.card.reviewers.set([self.user])

    def test_done_button_does_not_show_for_project_cards(self):
        self.make_project_card()
        self.page.wait_for_load_state("networkidle")
        
        ip_column = self.page.text_content("div#column_IP")
        self.assertNotIn("Done", ip_column)

    def test_done_button_shows_for_topic_cards(self):
        self.make_topic_card()

        self.page.wait_for_load_state("networkidle")
        ip_topic_card = self.page.text_content("div#column_IP")
        
        self.assertIn("Done", ip_topic_card)

    def test_done_button_moves_ip_topic_card_to_complete_column(self):
        self.make_topic_card()
        self.page.click("text=Done")

        self.page.wait_for_load_state("networkidle")

        ip_column = self.page.text_content("div#column_IP")
        complete_column = self.page.text_content("div#column_C")
        
        card_title = self.card.content_item.title

        self.assertIn(card_title, complete_column)
        self.assertNotIn(card_title, ip_column)

    def test_cannot_finish_topic_with_outstanding_card_reviews(self):
        self.make_outstanding_ir_project_card()
        self.make_topic_card()

        self.page.click("text=Done")

        self.page.wait_for_load_state("networkidle")

        self.assertIn(
            "You have outstanding card reviews", self.page.text_content("div#column_IP")
        )

    def test_done_button_logs_finish_topic_event(self):
        self.make_topic_card()

        self.page.click("text=Done")

        self.page.wait_for_load_state("networkidle")

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, self.user)
        self.assertEqual(entry.effected_user, self.card.assignees.first())
        self.assertEqual(entry.object_1, self.card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_MOVED_TO_COMPLETE)
