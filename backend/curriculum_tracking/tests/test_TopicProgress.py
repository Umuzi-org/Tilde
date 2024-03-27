from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from unittest.mock import patch

from curriculum_tracking.tests import factories
from curriculum_tracking.models import AgileCard, ContentItem
from activity_log.models import LogEntry
import curriculum_tracking.activity_log_entry_creators as log_creators


class TestTopicProgress(TestCase):

    def test_duration_str_returns_none_when_there_are_no_log_entries(self):
        user = factories.UserFactory(is_superuser=False)
        card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )

        card.assignees.set([user])
        card.start_topic()
        self.assertIn("duration_str", dir(card.topic_progress))
        self.assertEquals(card.topic_progress.duration_str, None)

    def test_duration_str_returns_correct_duration(self):
        user = factories.UserFactory(is_superuser=False)
        card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )

        card.assignees.set([user])
        card.start_topic()

        with patch.object(
            LogEntry._meta.get_field("timestamp"), "auto_now_add", True
        ), patch(
            "django.utils.timezone.now",
            side_effect=[
                timezone.now(),
                timezone.now(),
                timezone.now(),
                timezone.now() + timedelta(hours=3),
            ],
        ):
            log_creators.log_card_started(card=card, actor_user=user)
            log_creators.log_card_moved_to_complete(card=card, actor_user=user)

            card.status = "C"

            self.assertEquals(
                card.topic_progress.duration_str, "0 days, 3 hours, 0 minutes"
            )
