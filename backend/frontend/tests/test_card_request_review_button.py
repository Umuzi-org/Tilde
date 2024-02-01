from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory, ContentItemFactory
from curriculum_tracking.models import ContentItem, AgileCard
from .frontend_test_mixin import FrontendTestMixin


class TestCardRequestReviewButton(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()

        self.do_login(self.user)

    def make_outstanding_ir_project_card(self, project_submission_type):
        self.card: AgileCard = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=project_submission_type,
            ),
            status=AgileCard.IN_REVIEW,
        )
        self.card.reviewers.set([self.user])

    def make_ip_topic_card(self):
        self.card: AgileCard = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.TOPIC, topic_needs_review=True
            ),
            status=AgileCard.IN_PROGRESS,
        )
        self.card.assignees.set([self.user])

    def make_ip_project_card(self, project_submission_type):
        self.card: AgileCard = AgileCardFactory(
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

    def test_request_review_button_does_not_show_for_topic_cards(self):
        self.make_ip_topic_card()

        ip_column = self.page.text_content("div#column_IP")

        self.assertNotIn("Request Review", ip_column)

    def test_request_review_button_moves_ip_project_card_to_ir_column(self):
        self.make_ip_project_card(ContentItem.LINK)

        self.page.click("text=Request Review")

        self.page.wait_for_load_state("networkidle")

        ip_column = self.page.text_content("div#column_IP")
        review_column = self.page.text_content("div#column_IR")
        card_title = self.card.content_item.title

        self.assertIn(card_title, review_column)
        self.assertNotIn(card_title, ip_column)

    def test_request_review_button_moves_rf_project_card_to_ir_column(self):
        self.make_rf_project_card(ContentItem.LINK)

        self.page.click("text=Request Review")

        self.page.wait_for_load_state("networkidle")

        rf_column = self.page.text_content("div#column_RF")
        review_column = self.page.text_content("div#column_IR")
        card_title = self.card.content_item.title

        self.assertIn(card_title, review_column)
        self.assertNotIn(card_title, rf_column)

    def test_cannot_request_review_with_outstanding_card_reviews(self):
        self.make_outstanding_ir_project_card(ContentItem.LINK)
        self.make_ip_project_card(ContentItem.LINK)

        self.page.click("text=Request Review")

        self.page.wait_for_load_state("networkidle")

        self.assertIn(
            "You have outstanding card reviews", self.page.text_content("div#column_IP")
        )
