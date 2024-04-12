from core.tests.factories import UserFactory
from playwright.sync_api import expect
from .frontend_test_mixin import FrontendTestMixin
from django.urls import reverse_lazy


class TestLoginLogout(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="learner_login@umuzi.org",
            is_staff=True,
        )
        self.user.set_password(self.user.email)
        self.user.save()

        self.url_requiring_login = self.reverse_url(
            "user_board", kwargs={"user_id": self.user.id}
        )

    def test_user_can_login(self):
        self.do_login(self.user)

        self.page.goto(self.url_requiring_login)

        body = self.page.locator("body")
        expect(body).to_contain_text(f"Viewing {self.user.email}")

    def test_user_can_logout(self):
        self.do_login(self.user)

        self.page.goto(self.url_requiring_login)

        self.page.click('button#user-menu-button')

        self.page.click("text=Sign out")

        self.page.goto(self.url_requiring_login)

        url_requiring_login_path = reverse_lazy("user_board", kwargs={"user_id": self.user.id})

        self.assertIn(f"?next={url_requiring_login_path}", self.page.url)

        body = self.page.locator("body")
        expect(body).to_contain_text("Login")
