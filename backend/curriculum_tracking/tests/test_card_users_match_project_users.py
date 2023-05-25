

from django.test import TestCase
from curriculum_tracking import models
from curriculum_tracking.tests import factories
from core.tests import factories as core_factories

# class TestCardsAndProjectsHaveSamePeople(TestCase):
#     def setUp(self):
#         self.project = factories.RecruitProjectFactory()
#         self.project.reviewer_users.add(core_factories.UserFactory())
#         self.card = factories.AgileCardFactory(
#             recruit_project = self.project,
#         )

#     def assertUsersLineUp(self):
#         card_assignees = sorted([o.id for o in self.card.assignees.all()])
#         card_reviewers = sorted([o.id for o in self.card.reviewers.all()])

#         project_assignees = sorted([o.id for o in self.project.recruit_users.all()])
#         project_reviewers = sorted([o.id for o in self.project.reviewer_users.all()])

#         self.assertEqual(card_assignees,project_assignees)
#         self.assertEqual(card_reviewers,project_reviewers)

#     def test_setup_makes_sense(self):
#         self.assertUsersLineUp()
        
    # def test_change_project_reviewers(self):
    #     existing = self.project.reviewer_users.first()
    #     self.project.reviewer_users.add(core_factories.UserFactory())
    #     self.assertUsersLineUp()
    #     self.project.reviewer_users.remove(existing)
    #     self.assertUsersLineUp()

    # def test_change_project_assignees(self):
    #     existing = self.project.recruit_users.first()
    #     self.project.recruit_users.add(core_factories.UserFactory())
    #     self.assertUsersLineUp()
    #     self.project.recruit_users.remove(existing)
    #     self.assertUsersLineUp()


    # def test_change_card_reviewers(self):
    #     existing = self.card.reviewers.first()
    #     self.card.reviewers.add(core_factories.UserFactory())
    #     self.assertUsersLineUp()
    #     self.card.reviewers.remove(existing)
    #     self.assertUsersLineUp()


    # def test_change_card_assignees(self):
    #     existing = self.card.assignees.first()
    #     self.card.assignees.add(core_factories.UserFactory())
    #     self.assertUsersLineUp()
    #     self.card.assignees.remove(existing)
    #     self.assertUsersLineUp()
        