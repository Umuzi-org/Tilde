from activity_log.models import LogEntry
from playwright.sync_api import expect
from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory, ContentItemFactory
from curriculum_tracking.models import ContentItem, AgileCard
import curriculum_tracking.activity_log_entry_creators as creators
from .frontend_test_mixin import FrontendTestMixin


class TestCardRequestReviewButton(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()


    def make_outstanding_ir_project_card(self, project_submission_type):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=project_submission_type,
            ),
            status=AgileCard.IN_REVIEW,
        )
        self.card.reviewers.set([self.user])

    def make_ip_project_card(self, project_submission_type):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=project_submission_type,
            ),
            status=AgileCard.IN_PROGRESS,
        )
        self.card.assignees.set([self.user])

    def make_rf_project_card(self, project_submission_type):
        self.card: AgileCard = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=project_submission_type,
            ),
            status=AgileCard.REVIEW_FEEDBACK,
        )
        self.card.assignees.set([self.user])

    def test_request_review_button_moves_ip_project_card_to_ir_column(self):
        self.make_ip_project_card(ContentItem.LINK)
        
        self.do_login(self.user)
        self.page.wait_for_load_state()

        self.page.locator("text=Request review").click()
        self.page.wait_for_load_state("networkidle")

        card_title = self.card.content_item.title
        expect(self.page.locator("div#column_IR")).to_contain_text(card_title)
        expect(self.page.locator("div#column_IP")).not_to_contain_text(card_title)

    def test_request_review_button_moves_rf_project_card_to_ir_column(self):
        self.make_rf_project_card(ContentItem.LINK)

        self.do_login(self.user)
        self.page.wait_for_load_state()

        self.page.locator("text=Request review").click()
        self.page.wait_for_load_state()

        card_title = self.card.content_item.title
        expect(self.page.locator("div#column_IR")).to_contain_text(card_title)
        expect(self.page.locator("div#column_RF")).not_to_contain_text(card_title)


    def test_cannot_request_review_with_outstanding_card_reviews(self):
        self.make_outstanding_ir_project_card(ContentItem.LINK)
        self.make_ip_project_card(ContentItem.LINK)

        self.do_login(self.user)
        self.page.wait_for_load_state()

        self.page.locator('text="Request review"').click();
        self.page.wait_for_load_state("networkidle")
        
        expect(self.page.locator("div#column_IP")).to_contain_text("You have outstanding card reviews")


    def test_request_review_button_logs_review_request_event(self):
        self.make_ip_project_card(ContentItem.LINK)

        self.do_login(self.user)
        self.page.wait_for_load_state()

        self.page.locator("text=Request review").click()
        self.page.wait_for_load_state("networkidle")

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, self.user)
        self.assertEqual(entry.effected_user, self.card.assignees.first())
        self.assertEqual(entry.object_1, self.card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_REVIEW_REQUESTED)
