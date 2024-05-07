from project_review_coordination.models import ProjectReviewBundleClaim
from core.tests.factories import UserFactory
from .frontend_test_mixin import FrontendTestMixin
from playwright.sync_api import expect


class TestClaimButtons(FrontendTestMixin):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="staff_1@umuzi.org",
            is_staff=True,
        )
        self.user.set_password(self.user.email)
        self.user.save()

        self.user_2 = UserFactory(email="staff_2@umuzi.org", is_staff=True)
        self.user_2.set_password(self.user_2.email)
        self.user_2.save()

        self.do_login(self.user)

    def test_buttons_displayed_when_claimant(self):
        ProjectReviewBundleClaim.objects.create(claimed_by_user=self.user)
        url = self.reverse_url("project_review_coordination_my_claims")

        self.page.goto(url)
        self.page.wait_for_load_state()
        body = self.page.locator("body")

        expect(body).to_contain_text("Add 15 minutes")
        expect(body).to_contain_text("Unclaim bundle")

    def test_buttons_not_displayed_when_not_claimant(self):
        ProjectReviewBundleClaim.objects.create(claimed_by_user=self.user_2)
        url = self.reverse_url("project_review_coordination_all_claims")
        self.page.goto(url)
        body = self.page.locator("body")

        expect(body).not_to_contain_text("Add 15 minutes")
        expect(body).not_to_contain_text("Unclaim bundle")
