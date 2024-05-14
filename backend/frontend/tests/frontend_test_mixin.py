"""
Test mixin used for frontend testing. This makes use of Playwright to test the frontend.

Based in https://github.com/mxschmitt/python-django-playwright/blob/master/test_login.py

StaticLiveServerTestCase is described here:
https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
"""

import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from django.urls import reverse
from core.tests.factories import UserFactory


class FrontendTestMixin(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self) -> None:
        super().tearDown()
        self.page.close()

    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def reverse_url(
        self, viewname, urlconf=None, args=None, kwargs=None, current_app=None
    ):
        """A wrapper around Django's reverse function that returns a full URL"""
        end = reverse(viewname, urlconf, args, kwargs, current_app)
        return f"{self.live_server_url}{end}"

    def do_login(self, user):
        """
        logs the user in. Assumes the email address ands password are the same.
        self.page will be on the page after login
        """
        self.page.goto(f"{self.live_server_url}/login/")
        self.page.fill("[name=username]", user.email)
        self.page.fill("[name=password]", user.email)
        self.page.click("text=Log in")


class SuperuserLoggedInFrontendTestCase(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(is_superuser=True)
        self.user.set_password(self.user.email)
        self.user.save()
        self.do_login(self.user)
