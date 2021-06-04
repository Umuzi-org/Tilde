from django.test import TestCase
from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import AgileCardFactory


class TestDeactivateUSerClearsReviewerDuties(TestCase):
    def test_user_removed_as_reviewer(self):
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

    def test_reviewers_removed_from_user_cards(self):
        user = UserFactory()

        cards = [AgileCardFactory(assignees=[user]) for i in range(2)]
        for card in cards:
            card.recruit_project.recruit_users.set([user])
            reviewer = UserFactory()
            card.reviewers.set([reviewer])
            card.recruit_project.reviewer_users.set([reviewer])

        # simply saving the user should have no effect
        user.save()

        for card in cards:
            project = card.recruit_project
            self.assertEqual(card.reviewers.count(), 1)
            self.assertEqual(card.assignees.first(), user)
            self.assertEqual(project.reviewer_users.count(), 1)
            self.assertEqual(project.recruit_users.first(), user)

        # but if we deactivate the user then nobody needs to review them
        user.active = False
        print("=======================")
        print("=======================")

        user.save()

        for card in cards:
            project = card.recruit_project
            self.assertEqual(card.reviewers.count(), 0)
            self.assertEqual(project.reviewer_users.count(), 0)
