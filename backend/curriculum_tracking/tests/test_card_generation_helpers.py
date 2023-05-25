from django.test import TestCase
from curriculum_tracking import models
from curriculum_tracking.tests import factories

from curriculum_tracking.card_generation_helpers import (
    _recurse_generate_ordered_content_items,
    create_or_update_content_cards_for_user,
    _get_or_create_or_update_card,
)
from core.tests import factories as core_factories
from django.utils import timezone
from taggit.models import Tag
from curriculum_tracking.constants import (
    RED_FLAG,
    NOT_YET_COMPETENT,
    COMPETENT,
    EXCELLENT,
)
from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)

JAVASCRIPT = "JAVASCRIPT"
PYTHON = "PYTHON"


class RegenerateCardsTests(TestCase):
    def setUp(self):
        # user = core_factories.UserFactory()
        registration = factories.CourseRegistrationFactory()
        registration2 = factories.CourseRegistrationFactory(
            curriculum=registration.curriculum
        )
        self.user1 = registration.user
        self.user2 = registration2.user
        self.curriculum = registration.curriculum
        self.content_item = factories.ProjectContentItemFactory(
            flavours=[JAVASCRIPT]
        )

        factories.CurriculumContentRequirementFactory(
            content_item=self.content_item,
            curriculum=self.curriculum,
            flavours=[JAVASCRIPT],
        )

    def test_generate_project_cards_twice_no_progress(self):
        generate_and_update_all_cards_for_user(self.user1, None)
        generate_and_update_all_cards_for_user(self.user1, None)

        cards = models.AgileCard.objects.all()
        self.assertEqual(cards.count(), 1)
        card = cards.first()
        self.assertIn(self.user1, card.assignees.all())

    def test_generate_project_cards_twice_has_progress(self):
        factories.RecruitProjectFactory(
            recruit_users=[self.user1],
            content_item=self.content_item,
            flavours=[JAVASCRIPT],
        )
        generate_and_update_all_cards_for_user(self.user1, None)
        generate_and_update_all_cards_for_user(self.user1, None)
        cards = models.AgileCard.objects.all()

        self.assertEqual(cards.count(), 1)
        card = cards.first()
        self.assertIn(self.user1, card.assignees.all())

    def test_generate_project_cards_twice_has_progress_multiple_assignees(self,):

        factories.RecruitProjectFactory(
            recruit_users=[self.user1, self.user2],
            content_item=self.content_item,
            flavours=[JAVASCRIPT],
        )
        generate_and_update_all_cards_for_user(self.user1, None)
        generate_and_update_all_cards_for_user(self.user1, None)

        cards = models.AgileCard.objects.all()
        self.assertEqual(cards.count(), 1)

        generate_and_update_all_cards_for_user(self.user2, None)
        generate_and_update_all_cards_for_user(self.user2, None)

        cards = models.AgileCard.objects.all()
        self.assertEqual(cards.count(), 1)
        card = cards.first()
        self.assertIn(self.user1, card.assignees.all())
        self.assertIn(self.user2, card.assignees.all())
