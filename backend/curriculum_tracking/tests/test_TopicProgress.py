from django.test import TestCase

from curriculum_tracking.tests import factories


class TestTopicProgress(TestCase):

    def test_duration_returns_none_when_there_are_no_log_entries(self):
        topic = factories.TopicProgressFactory()
        self.assertIn("duration", dir(topic))
        self.assertEquals(topic.duration, None)
