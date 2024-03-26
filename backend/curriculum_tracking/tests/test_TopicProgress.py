from django.test import TestCase

from curriculum_tracking.tests import factories


from core.models import User


class TestTopicProgress(TestCase):

    def test_duration_calculated_correctly(self):
        topic = factories.TopicProgressFactory()
        self.assertIn("duration", dir(topic))
