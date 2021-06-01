from django.test import TestCase
from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory


class TestDeactivateUSerClearsReviewerDuties(TestCase):
    def test_it(self):
        user = UserFactory()

        cards = [AgileCardFactory() for i in range(2)]

        for card in cards:
            project = card.recruit_project
            project.reviewer_users.add(user)
            project.save()
            card.reviewers.add(user)
            card.save()

        # simply saving the user should have no effect
        user.save()

        for card in cards:
            project = card.recruit_project
            self.assertIn(user, card.reviewers.all())
            self.assertIn(user, project.reviewer_users.all())

        # but if we deactivate the user then they are removed from all the things
        user.active = False
        user.save()

        for card in cards:
            project = card.recruit_project
            self.assertNotIn(user, card.reviewers.all())
            self.assertNotIn(user, project.reviewer_users.all())
