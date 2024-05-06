from django.test import TestCase, Client
from django.urls import reverse
from project_review_coordination.models import ProjectReviewBundleClaim
from core.tests.factories import UserFactory


class TestMyClaimsPage(TestCase):
    def setUp(self):

        super().setUp()
        self.user = UserFactory(
            email="staff_1@umuzi.org",
            is_staff=True,
        )
        self.user.set_password(self.user.email)
        self.user.save()

        # login user
        self.client = Client()
        self.client.login(email=self.user.email, password=self.user.email)

        # bundle claimed by user
        self.claim = ProjectReviewBundleClaim.objects.create(claimed_by_user=self.user)
        self.url = reverse("project_review_coordination_my_claims")

    def test_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_button_in_page(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Add 15 minutes")
        self.assertContains(response, "Unclaim bundle")
