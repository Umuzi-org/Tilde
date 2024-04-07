from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta

from curriculum_tracking.tests import factories
from curriculum_tracking.models import AgileCard, ContentItem


class get_total_duration(TestCase):
    def test_returns_correct_duration(self):
        card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )

        card.topic_progress.start_time = datetime(
            2024, 2, 12, 14, 6, 17, 373514, tzinfo=timezone.utc
        )
        card.topic_progress.end_time = datetime(
            2024, 2, 12, 15, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.assertEquals(
            card.topic_progress.get_total_duration, timedelta(seconds=3600)
        )
