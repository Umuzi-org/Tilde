from core.tests.factories import UserFactory, TeamFactory
from .frontend_test_mixin import FrontendTestMixin


class TestLoginLogout(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="learner@umuzi.org",
            is_staff=True,
            is_superuser=True,  # TODO: remove this once "restricted access" PR is merged
        )
        self.user.set_password(self.user.email)
        self.user.save()

        self.url_requiring_login = self.reverse_url(
            "user_board", kwargs={"user_id": self.user.id}
        )

    def test_user_can_login(self):
        self.do_login(self.user)

        self.page.goto(self.url_requiring_login)

        body = self.page.text_content("body")
        self.assertIn(f"Viewing {self.user.email}", body)

    def test_user_can_logout(self):
        self.do_login(self.user)

        self.page.goto(self.url_requiring_login)

        self.page.click('button#user-menu-button')

        self.page.click("text=Sign out")

        self.page.goto(self.url_requiring_login)

        body = self.page.text_content("body")
        self.assertIn("Login", body)
