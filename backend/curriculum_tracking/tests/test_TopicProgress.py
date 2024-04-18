from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime
from unittest.mock import patch

from curriculum_tracking.tests import factories
from curriculum_tracking import models


class duration_Tests(TestCase):

    def make_project_card(self, status):
        content_item = factories.ContentItemFactory(
            content_type=models.ContentItem.TOPIC
        )
        self.card = factories.AgileCardFactory(
            content_item=content_item,
            status=status,
        )

        self.card.topic_progress = models.TopicProgress(content_item=content_item)

    def test_returns_correct_duration_for_cards_unstarted(self):
        self.make_project_card(models.AgileCard.READY)

        self.assertEquals(self.card.topic_progress.duration, timedelta(seconds=0))

    @patch("django.utils.timezone.now")
    def test_returns_correct_duration_for_cards_in_progress(self, mock_now):
        mock_now.return_value = datetime(
            2024, 2, 16, 15, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.make_project_card(models.AgileCard.IN_PROGRESS)
        self.card.topic_progress.start_time = datetime(
            2024, 2, 12, 15, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.assertEquals(self.card.topic_progress.duration, timedelta(days=4))

    @patch("django.utils.timezone.now")
    def test_returns_correct_duration_for_cards_in_review_feedback(self, mock_now):
        mock_now.return_value = datetime(
            2024, 2, 16, 15, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.make_project_card(models.AgileCard.REVIEW_FEEDBACK)
        self.card.topic_progress.start_time = datetime(
            2024, 2, 12, 15, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.assertEquals(self.card.topic_progress.duration, timedelta(days=4))

    @patch("django.utils.timezone.now")
    def test_returns_correct_duration_for_cards_in_review(self, mock_now):
        mock_now.return_value = datetime(
            2024, 2, 16, 15, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.make_project_card(models.AgileCard.IN_REVIEW)
        self.card.topic_progress.start_time = datetime(
            2024, 2, 12, 15, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.assertEquals(self.card.topic_progress.duration, timedelta(days=4))

    def test_returns_correct_duration_for_cards_completed(self):
        self.make_project_card(models.AgileCard.COMPLETE)

        self.card.topic_progress.start_time = datetime(
            2024, 2, 12, 14, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.card.topic_progress.end_time = datetime(
            2024, 2, 12, 15, 6, 17, 373514, tzinfo=timezone.utc
        )

        self.assertEquals(self.card.topic_progress.duration, timedelta(seconds=3600))
