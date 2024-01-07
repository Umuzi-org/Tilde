import re
from urllib.parse import urlparse

from django.core import mail

from core.tests.factories import UserFactory
from .frontend_test_mixin import FrontendTestMixin


class TestForgotPassword(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="learner@umuzi.org",
            is_staff=True,
            is_superuser=True,  # TODO: remove this once "restricted access" PR is merged
        )
        self.user.set_password(self.user.email)
        self.user.save()

        self.non_existant_user_email = "non_existant_user@umuzi.org"

    def test_sends_password_reset_email_if_user_exists(self):
        self.page.goto(self.reverse_url("user_login"))

        self.page.click("text=Forgot Password?")

        self.page.fill("[name=email]", self.user.email)
        self.page.click("text=Reset Password")

        self.assertEqual(len(mail.outbox), 1)

        sent_email = mail.outbox[0]
        self.assertIn("Reset your Password", sent_email.subject)
        self.assertEqual([self.user.email], sent_email.to)

        url_pattern = re.compile(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        )

        extracted_url = url_pattern.search(sent_email.body).group()
        extracted_url = urlparse(extracted_url)

        self.page.goto(f"{self.live_server_url}{extracted_url.path}")

        reset_page_body = self.page.text_content("body")
        self.assertIn("New password", reset_page_body)

    def test_does_not_send_password_reset_email_if_user_does_not_exist(self):
        self.page.goto(self.reverse_url("user_login"))

        self.page.click("text=Forgot Password?")

        self.page.fill("[name=email]", self.non_existant_user_email)
        self.page.click("text=Reset Password")

        # Ensure no email was sent
        self.assertEqual(len(mail.outbox), 0)
