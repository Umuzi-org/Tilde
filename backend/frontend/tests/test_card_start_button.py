from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory, ContentItemFactory
from curriculum_tracking.models import ContentItem, AgileCard
from .frontend_test_mixin import FrontendTestMixin


class TestCardStartButton(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="learner@umuzi.org",
            is_staff=True,
            is_superuser=True,  # TODO: remove this once "restricted access" PR is merged
        )
        self.user.set_password(self.user.email)
        self.user.save()

        self.do_login(self.user)
        # url = self.reverse_url("user_board")
        # self.page.goto(url)

        self.backlog_column = self.page.get_by_role("div").and_(
            self.page.get_by_title("Backlog")
        )
        self.ip_column = self.page.get_by_role("div").and_(
            self.page.get_by_title("In Progress")
        )

    def make_topic_card(self):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )
        self.card.assignees.set([self.user])

    def make_project_card(self, content_type):
        self.card = AgileCardFactory(
            content_item=ContentItemFactory(
                content_type=content_type,
                project_submission_type=ContentItem.PROJECT,
            ),
            status=AgileCard.READY,
        )
        self.card.assignees.set([self.user])

    def test_start_button_moves_topic_card_to_ip_column(self):
        self.make_topic_card()
        start_button = self.page.get_by_role("button").and_(
            self.page.get_by_title("Start")
        )

        print(self.card)
        print(self.backlog_column)
        print(self.ip_column)
        print(start_button)

    def test_start_button_moves_project_card__to_ip_column(self):
        self.make_project_card(content_type=ContentItem.PROJECT)
        self.make_project_card(content_type=ContentItem.LINK)
        start_button = self.page.get_by_role("button").and_(
            self.page.get_by_title("Start")
        )

        print(self.card)
        print(self.backlog_column)
        print(self.ip_column)
        print(start_button)
