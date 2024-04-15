from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import (
    AgileCardFactory,
    ContentItemFactory,
)
from playwright.sync_api import expect
from curriculum_tracking.models import ContentItem, AgileCard
from .frontend_test_mixin import FrontendTestMixin
from activity_log.models import LogEntry
import curriculum_tracking.activity_log_entry_creators as creators


class TestCardCancelReviewRequestButton(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()

    def make_project_card(self, project_submission_type):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=project_submission_type,
            ),
            status=AgileCard.IN_REVIEW,
        )

        self.card.assignees.set([self.user])

    def test_cancel_review_request_button_moves_project_card_to_ip_column(self):
        self.make_project_card(ContentItem.LINK)

        self.do_login(self.user)
        self.page.wait_for_load_state()

        self.page.locator('text="Cancel review request"').click();
        self.page.wait_for_load_state("networkidle")

        project_card_title = self.card.content_item.title

        expect(self.page.locator("div#column_IP")).to_contain_text(project_card_title)
        expect(self.page.locator("div#column_IR")).not_to_contain_text(project_card_title)


    def test_cancel_review_request_button_logs_card_review_request_cancelled_event(
        self,
    ):
        self.make_project_card(ContentItem.LINK)
        
        self.do_login(self.user)
        self.page.wait_for_load_state()

        self.page.locator("text=Cancel review request").click()
        self.page.wait_for_load_state("networkidle")

        self.assertEqual(LogEntry.objects.count(), 1)
        entry = LogEntry.objects.first()

        self.assertEqual(entry.actor_user, self.user)
        self.assertEqual(entry.effected_user, self.card.assignees.first())
        self.assertEqual(entry.object_1, self.card.recruit_project)
        self.assertEqual(entry.object_2, None)
        self.assertEqual(entry.event_type.name, creators.CARD_REVIEW_REQUEST_CANCELLED)
