from django.test import TestCase
from curriculum_tracking.models import AgileCard
from curriculum_tracking.tests import factories
from core.tests import factories as core_factories


class request_user_is_trusted_Tests(TestCase):
    def setUp(self):
        self.user = core_factories.UserFactory()

        self.card_user_is_trusted_on_js_flavour = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS, flavours=[["javascript"]]
        )
        self.card_user_is_trusted_on_py_flavour = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS, flavours=[["python"]]
        )
        self.card_user_is_trusted_on_no_flavour = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS, flavours=[]
        )

        trusted_cards = [
            self.card_user_is_trusted_on_js_flavour,
            self.card_user_is_trusted_on_py_flavour,
            self.card_user_is_trusted_on_no_flavour,
        ]

        for trusted_card in trusted_cards:
            trust = factories.ReviewTrustFactory(
                content_item=trusted_card.content_item,
                flavours=[o.name for o in trusted_card.flavours.all()],
                user=self.user,
            )

        self.card_user_is_not_trusted_on_js_flavour = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS
        )
        self.card_user_is_not_trusted_on_py_flavour = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS
        )
        self.card_user_is_not_trusted_on_no_flavour = factories.AgileCardFactory(
            status=AgileCard.IN_PROGRESS
        )

    def test_request_user_is_trusted_on_flavoured_cards(self):
        pass

    def test_request_user_is_trusted_on_not_flavoured_cards(self):
        pass
