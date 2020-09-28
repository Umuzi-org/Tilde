from django.test import TestCase
from curriculum_tracking import models
from curriculum_tracking.tests import factories


class ContentItemRelationshipTests(TestCase):
    def test_relationship_is_in_correct_order(self):

        item1 = factories.ContentItemFactory()
        item2 = factories.ContentItemFactory()

        # item 1 as a prerequisite to item 2
        order = factories.ContentItemOrderFactory(pre=item1, post=item2)

        prereq_1 = list(item1.prerequisites.all())
        unlocks_1 = list(item1.unlocks.all())
        post_order_1 = list(item1.post_ordered_content.all())
        pre_order_1 = list(item1.pre_ordered_content.all())

        assert post_order_1 == [order], post_order_1
        assert pre_order_1 == [], pre_order_1
        assert prereq_1 == [], prereq_1
        assert unlocks_1 == [item2], unlocks_1

        prereq_2 = list(item2.prerequisites.all())
        unlocks_2 = list(item2.unlocks.all())

        assert prereq_2 == [item1], prereq_2
        assert unlocks_2 == [], unlocks_2

        assert item2.all_prerequisite_content_items() == [item1]
