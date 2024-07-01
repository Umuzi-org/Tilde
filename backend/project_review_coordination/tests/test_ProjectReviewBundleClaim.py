from core.tests.factories import UserFactory
from django.test import TestCase

from .factories import ProjectReviewBundleClaimFactory


class request_user_can_unclaim_Tests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.claim = ProjectReviewBundleClaimFactory(claimed_by_user=self.user)

    def test_claimed_by_user_can_unclaim(self):
        self.assertTrue(self.claim.request_user_can_unclaim(self.user))

    def test_superuser_can_unclaim(self):
        superuser = UserFactory(is_superuser=True)
        self.assertTrue(self.claim.request_user_can_unclaim(superuser))

    def test_other_user_cannot_unclaim(self):
        other_user = UserFactory()
        self.assertFalse(self.claim.request_user_can_unclaim(other_user))
