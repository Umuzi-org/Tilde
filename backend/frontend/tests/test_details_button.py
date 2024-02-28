from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory, ContentItemFactory
from curriculum_tracking.models import ContentItem, AgileCard
from .frontend_test_mixin import FrontendTestMixin
from playwright.sync_api import expect


class TestCardDetailsButton(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()

        self.do_login(self.user)

    def make_topic_card(self):
        self.card: AgileCard = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.TOPIC, topic_needs_review=True
            ),
            status=AgileCard.IN_PROGRESS,
        )
        self.card.assignees.set([self.user])

    def make_project_card(self, project_submission_type):
        self.card: AgileCard = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=project_submission_type,
            ),
            status=AgileCard.IN_PROGRESS,
        )
        self.card.assignees.set([self.user])

    def test_details_button_redirects_to_link_project_details_page(self):
        self.make_project_card(ContentItem.LINK)

        link_card_element = self.page.locator("#column_IP > #card_1")
        details_link_element = link_card_element.get_by_role("link", name="Details")

        expect(link_card_element).to_be_visible()
        expect(details_link_element).to_be_visible()

        self.assertEqual(
            details_link_element.get_attribute("href"),
            "#",
        )
