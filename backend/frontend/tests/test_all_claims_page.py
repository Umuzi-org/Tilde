from django.test import TestCase, Client
from django.urls import reverse
from project_review_coordination.models import ProjectReviewBundleClaim
from core.tests.factories import UserFactory


class TestAllClaimsPage(TestCase):
    def setUp(self):

        super().setUp()
        self.user = UserFactory(
            email="staff_1@umuzi.org",
            is_staff=True,
        )
        self.user.set_password(self.user.email)
        self.user.save()

        # user 2
        self.user_2 = UserFactory(email="staff_2@umuzi.org", is_staff=True)
        self.user_2.set_password(self.user_2.email)
        self.user_2.save()
        # user login
        self.client = Client()
        self.client.login(email=self.user.email, password=self.user.email)
        # claimed by user 2
        self.claim = ProjectReviewBundleClaim.objects.create(
            claimed_by_user=self.user_2
        )
        self.url = reverse("project_review_coordination_all_claims")

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # test that when user is not the claimant, the buttons are not displayed in the all claims page
    def test_buttons_not_displayed(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "Add 15 minutes")
        self.assertNotContains(response, "Unclaim bundle")
