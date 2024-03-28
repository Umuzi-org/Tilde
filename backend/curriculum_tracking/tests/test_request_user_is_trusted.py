from django.test import TestCase
from curriculum_tracking.models import AgileCard
from curriculum_tracking.tests import factories
from core.tests import factories as core_factories


class request_user_is_trusted_Tests(TestCase):
    def setUp(self):
        self.user = core_factories.UserFactory()

        self.card_user_is_trusted_on_js_flavours = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS, flavours=[["javascript"]]
        )
        self.card_user_is_trusted_on_py_flavours = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS, flavours=[["python"]]
        )
        self.card_user_is_trusted_on_no_flavours = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS, flavours=[]
        )

        self.trusted_cards = [
            self.card_user_is_trusted_on_js_flavours,
            self.card_user_is_trusted_on_py_flavours,
            self.card_user_is_trusted_on_no_flavours,
        ]

        for trusted_card in self.trusted_cards:
            factories.ReviewTrustFactory(
                content_item=trusted_card.content_item,
                flavours=[o.name for o in trusted_card.flavours.all()],
                user=self.user,
            )

    def test_request_user_is_trusted_on_cards(self):
        for card in self.trusted_cards:
            self.assertTrue(card.request_user_is_trusted(self.user))
