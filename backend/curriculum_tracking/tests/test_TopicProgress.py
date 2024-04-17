from django.test import TestCase
from django.utils import timezone
from datetime import timedelta,datetime

from curriculum_tracking.tests import factories
from curriculum_tracking.models import AgileCard, ContentItem



class duration_Tests(TestCase):
    pass

    # DATETIME_NONE_TYPEERROR_MESSAGE = "TypeError: unsupported operand type(s) for -: 'datetime.datetime' and 'NoneType'"

    # def make_project_card(self):
    #     self.card = factories.AgileCardFactory(
    #         content_item=factories.ContentItemFactory(content_type=ContentItem.TOPIC),
    #         status=AgileCard.READY,
    #     )


    # def test_returns_correct_value(self):
    #     self.make_project_card()

    #     self.card.topic_progress.start_time = datetime(
    #         2024, 2, 12, 14, 6, 17, 373514, tzinfo=timezone.utc
    #     )
   
    #     self.card.topic_progress.end_time = datetime(
    #         2024, 2, 12, 15, 6, 17, 373514, tzinfo=timezone.utc
    #     )

    #     self.assertEquals(self.card.topic_progress.duration, timedelta(seconds=3600))

    # def test_raises_typeerror_when_starttime_is_empty(self):
    #     self.make_project_card()

    #     self.card.topic_progress.start_time = None
    #     self.card.topic_progress.end_time = datetime(
    #         2024, 2, 12, 15, 6, 17, 373514, tzinfo=timezone.utc
    #     )

    #     self.assertRaisesMessage(
    #         TypeError,
    #         self.DATETIME_NONE_TYPEERROR_MESSAGE,
    #     )

    # def test_raises_typeerror_when_endtime_is_empty(self):
    #     self.make_project_card()

    #     self.card.topic_progress.start_time = datetime(
    #         2024, 2, 12, 15, 6, 17, 373514, tzinfo=timezone.utc
    #     )
    #     self.card.topic_progress.end_time = None

    #     self.assertRaisesMessage(
    #         TypeError,
    #         self.DATETIME_NONE_TYPEERROR_MESSAGE,
    #     )

    # def test_raises_typeerror_when_both_starttime_and_endtime_are_empty(self):
    #     self.make_project_card()

    #     self.card.topic_progress.start_time = None
    #     self.card.topic_progress.end_time = None

    #     self.assertRaisesMessage(
    #         TypeError,
    #         self.DATETIME_NONE_TYPEERROR_MESSAGE,
    #     )
