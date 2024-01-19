from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory, ContentItemFactory
from curriculum_tracking.models import ContentItem, AgileCard
from .frontend_test_mixin import FrontendTestMixin


class TestCardStartButton(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.user.set_password(self.user.email)
        self.user.save()

        self.do_login(self.user)

    def make_topic_card(self):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )

        # replace default assignee with our user
        self.card.assignees.first().delete()
        self.card.assignees.add(self.user)

    def make_project_card(self):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            status=AgileCard.READY,
        )

        # replace default assignee with our user
        self.card.assignees.first().delete()
        self.card.assignees.add(self.user)

    def test_start_button_moves_topic_card_to_ip_column(self):
        self.make_topic_card()

        can_start = self.card.request_user_can_start(self.user)

        if can_start:
            self.page.click("text=Start")

            self.page.wait_for_load_state("networkidle")

            ip_column = self.page.text_content("div#column_IP")
            backlog_column = self.page.text_content("div#column_RB")
            project_card_title = self.card.content_item.title

            self.assertIn(project_card_title, ip_column)
            self.assertNotIn(project_card_title, backlog_column)
