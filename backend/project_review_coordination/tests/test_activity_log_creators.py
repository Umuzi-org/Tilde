from unittest.mock import patch
from django.test import TestCase
import datetime
from django.utils import timezone

from core.tests.factories import UserFactory
from activity_log.models import LogEntry
from project_review_coordination import activity_log_creators as creators
from project_review_coordination.models import ProjectReviewBundleClaim

from .factories import ProjectReviewBundleClaimFactory


class review_bundle_claim_activity_log_Tests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_log_bundle_claimed(self):
        self.assertEqual(LogEntry.objects.all().count(), 0)

        ProjectReviewBundleClaimFactory(claimed_by_user=self.user)

        self.assertEqual(LogEntry.objects.all().count(), 1)

        log = LogEntry.objects.first()
        self.assertEqual(log.actor_user, self.user)
        self.assertEqual(log.effected_user, self.user)
        self.assertEqual(log.event_type.name, creators.BUNDLE_CLAIMED)

    def test_log_bundle_unclaimed(self):
        self.assertEqual(LogEntry.objects.all().count(), 0)

        claim = ProjectReviewBundleClaimFactory(claimed_by_user=self.user)
        claim.unclaim()

        self.assertEqual(
            LogEntry.objects.all().count(), 2
        )  # Includes the claim creation log

        log = LogEntry.objects.last()
        self.assertEqual(log.actor_user, self.user)
        self.assertEqual(log.effected_user, self.user)
        self.assertEqual(log.event_type.name, creators.BUNDLE_UNCLAIMED)

    def test_log_bundle_time_added(self):
        self.assertEqual(LogEntry.objects.all().count(), 0)

        claim = ProjectReviewBundleClaimFactory(claimed_by_user=self.user)
        claim.add_time()

        self.assertEqual(
            LogEntry.objects.all().count(), 2
        )  # Includes the claim creation log

        log = LogEntry.objects.last()
        self.assertEqual(log.actor_user, self.user)
        self.assertEqual(log.effected_user, self.user)
        self.assertEqual(log.event_type.name, creators.TIME_ADDED)

    def test_log_bundle_expired(
        self,
    ):
        self.assertEqual(LogEntry.objects.all().count(), 0)

        claim = ProjectReviewBundleClaimFactory(claimed_by_user=self.user)
        expired_by_timestamp = claim.due_timestamp + datetime.timedelta(minutes=10)

        ProjectReviewBundleClaim.deactivate_expired_claims(
            by_timestamp=expired_by_timestamp
        )

        self.assertEqual(
            LogEntry.objects.all().count(), 2
        )  # Includes the claim creation log

        log = LogEntry.objects.last()
        self.assertEqual(log.actor_user, None)
        self.assertEqual(log.effected_user, self.user)
        self.assertEqual(log.event_type.name, creators.BUNDLE_EXPIRED)
