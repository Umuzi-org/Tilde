from datetime import timedelta
from django.test import TestCase
from core.tests.factories import UserFactory
from . import factories
from curriculum_tracking.models import AgileCard, BurndownSnapshot, ContentItem


class create_snapshot_Tests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_taking_multiple_snapshots_quickly_only_makes_once_instance(self):
        BurndownSnapshot.create_snapshot(user=self.user)
        BurndownSnapshot.create_snapshot(user=self.user)

        self.assertEqual(BurndownSnapshot.objects.count(), 1)

    def test_taking_multiple_snapshots_slowly_makes_multiple_instances(self):
        snapshot = BurndownSnapshot.create_snapshot(user=self.user)

        snapshot.timestamp = snapshot.timestamp - timedelta(
            hours=BurndownSnapshot.MIN_HOURS_BETWEEN_SNAPSHOTS + 1
        )
        snapshot.save()

        BurndownSnapshot.create_snapshot(user=self.user)

        self.assertEqual(BurndownSnapshot.objects.count(), 2)

    def test_calculations_correct(self):
        # some topics
        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            assignees=[self.user],
        )
        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            assignees=[self.user],
            status=AgileCard.COMPLETE,
        )

        # some projects
        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            assignees=[self.user],
        )
        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            assignees=[self.user],
            status=AgileCard.COMPLETE,
        )

        BurndownSnapshot.create_snapshot(user=self.user)
        snapshot = BurndownSnapshot.objects.first()

        self.assertEqual(snapshot.user, self.user)
        self.assertEqual(snapshot.cards_total_count, 4)
        self.assertEqual(snapshot.project_cards_total_count, 2)
        self.assertEqual(snapshot.cards_in_complete_column_total_count, 2)
        self.assertEqual(snapshot.project_cards_in_complete_column_total_count, 1)

    def test_snapshot_saves_latest_data(self):

        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            assignees=[self.user],
        )
        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            assignees=[self.user],
            status=AgileCard.COMPLETE,
        )

        # BurndownSnapshot.create_snapshot(user=self.user)
        # snapshot = BurndownSnapshot.objects.first()

        # snapshot.timestamp = snapshot.timestamp - timedelta(
        #     hours=BurndownSnapshot.MIN_HOURS_BETWEEN_SNAPSHOTS + 1
        # )
        # snapshot.save()

        # self.assertEqual(snapshot.user, self.user)
        # self.assertEqual(snapshot.cards_total_count, 2)
        # self.assertEqual(snapshot.project_cards_total_count, 2)
        # self.assertEqual(snapshot.cards_in_complete_column_total_count, 1)
        # self.assertEqual(snapshot.project_cards_in_complete_column_total_count, 1)

        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            assignees=[self.user],
        )
        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            assignees=[self.user],
            status=AgileCard.COMPLETE,
        )

        BurndownSnapshot.create_snapshot(user=self.user)
        # snapshot = BurndownSnapshot.objects.first()
        # snapshot.save()

        factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            assignees=[self.user],
            status=AgileCard.COMPLETE,
        )

        BurndownSnapshot.create_snapshot(user=self.user)
        snapshot = BurndownSnapshot.objects.first()
        snapshot.save()


        self.assertEqual(BurndownSnapshot.objects.count(), 1)
        self.assertEqual(snapshot.user, self.user)
        self.assertEqual(snapshot.cards_total_count, 5)
        self.assertEqual(snapshot.project_cards_total_count, 3)
        self.assertEqual(snapshot.cards_in_complete_column_total_count, 3)
        self.assertEqual(snapshot.project_cards_in_complete_column_total_count, 2)