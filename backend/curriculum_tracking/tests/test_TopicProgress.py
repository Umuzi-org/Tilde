from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from unittest.mock import patch

from curriculum_tracking.tests import factories
from curriculum_tracking.models import AgileCard, ContentItem
from activity_log.models import LogEntry
import curriculum_tracking.activity_log_entry_creators as log_creators


class TestTopicProgress(TestCase):

    def test_duration_returns_none_when_there_are_no_log_entries(self):
        topic = factories.TopicProgressFactory()
        self.assertIn("duration", dir(topic))
        self.assertEquals(topic.duration, None)

    def test_duration_returns_correct_duration(self):
        user = factories.UserFactory(is_superuser=False)
        card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
            status=AgileCard.READY,
        )

        card.assignees.set([user])
        card.start_topic()
        log_creators.log_card_moved_to_complete(card=card, actor_user=user)

        with patch.object(
            LogEntry._meta.get_field("timestamp"), "auto_now_add", True
        ), patch(
            "django.utils.timezone.now",
            side_effect=[
                timezone.now(),
                timezone.now() + timedelta(hours=3),
            ],
        ):

            pass
