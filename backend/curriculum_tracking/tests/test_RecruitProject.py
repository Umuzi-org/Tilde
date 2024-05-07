from core.tests.factories import TeamFactory, UserFactory
from django.test import TestCase

from curriculum_tracking import models
from curriculum_tracking.tests import factories
from curriculum_tracking.constants import COMPETENT, EXCELLENT
from core.tests import factories as core_factories
from core.models import Team
from guardian.shortcuts import assign_perm

JAVASCRIPT = "js"
TYPESCRIPT = "ts"


from core.models import User


class get_users_with_permission_Tests(TestCase):
    def setUp(self):
        self.project_assignee_user = UserFactory(is_superuser=False)
        self.assignee_team = TeamFactory()
        self.assignee_team.users.add(self.project_assignee_user)

        self.project_reviewer_user = UserFactory(is_superuser=False)
        self.reviewer_team = TeamFactory()
        self.reviewer_team.users.add(self.project_reviewer_user)

        self.permissioned_user = UserFactory(is_superuser=False)
        self.permissioned_team = TeamFactory()
        self.permissioned_team.users.add(self.permissioned_user)

        self.project = factories.RecruitProjectFactory(
            recruit_users=[self.project_assignee_user],
            reviewer_users=[self.project_reviewer_user],
        )

    def test_no_permissions_given(self):
        users = self.project.get_users_with_permission(Team.PERMISSION_MANAGE_CARDS)
        self.assertEqual(users, [])

    def test_user_has_direct_permission_on_assignees_team(self):
        assign_perm(
            Team.PERMISSION_MANAGE_CARDS, self.permissioned_user, self.assignee_team
        )
        users = self.project.get_users_with_permission(Team.PERMISSION_MANAGE_CARDS)
        self.assertEqual(users, [self.permissioned_user])

    def test_user_has_direct_permission_on_reviewers_team(self):
        assign_perm(
            Team.PERMISSION_MANAGE_CARDS, self.permissioned_user, self.reviewer_team
        )
        users = self.project.get_users_with_permission(Team.PERMISSION_VIEW)
        self.assertEqual(users, [self.permissioned_user])


class generate_repo_name_for_project_Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="fooo@bar.com",
            first_name="fooo",
            last_name="baaar",
            password="top_secret",
        )

    def test_length_ok(self):
        project = factories.ProjectContentItemFactory()
        repo_name = models.RecruitProject._generate_repo_name_for_project(
            user=self.user, content_item=project, flavour_names=["javascript", "react"]
        )

        self.assertIn(str(project.id), repo_name)
        self.assertIn(project.slug, repo_name)
        self.assertIn(self.user.first_name, repo_name)
        self.assertIn(self.user.last_name, repo_name)

    def test_too_long(self):
        project = factories.ProjectContentItemFactory(title="test project " * 10)
        self.assertGreater(len(project.slug), 100)
        repo_name = models.RecruitProject._generate_repo_name_for_project(
            user=self.user, content_item=project, flavour_names=[]
        )

        self.assertIn(str(project.id), repo_name)
        self.assertIn("-test-project-", repo_name)
        self.assertIn(self.user.first_name, repo_name)
        self.assertIn(self.user.last_name, repo_name)


class request_user_can_add_review_Tests(TestCase):
    def setUp(self):
        self.assignee_user = UserFactory()
        self.reviewer_user = UserFactory()
        self.random_reviewer = UserFactory()
        self.user_with_permissions = UserFactory()
        self.superuser = UserFactory(
            is_superuser=True
        )

        self.assignee_team = core_factories.TeamFactory()
        self.assignee_team.user_set.add(self.assignee_user)
        self.assignee_team.save()

        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            self.user_with_permissions,
            self.assignee_team,
        )

        self.in_review_project_card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=models.ContentItem.PROJECT,
                project_submission_type=models.ContentItem.LINK,
            ),
            status=models.AgileCard.IN_REVIEW,
        )
        self.in_review_project_card.assignees.add(self.assignee_user)
        self.in_review_project_card.reviewers.add(self.reviewer_user)

        self.complete_project_card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=models.ContentItem.PROJECT,
                project_submission_type=models.ContentItem.LINK,
            ),
            status=models.AgileCard.COMPLETE,
        )
        self.complete_project_card.assignees.add(self.assignee_user)
        self.complete_project_card.reviewers.add(self.reviewer_user)
        self.complete_project_card.reviewers.add(self.random_reviewer)

        self.review_feedback_project_card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=models.ContentItem.PROJECT,
                project_submission_type=models.ContentItem.LINK,
            ),
            status=models.AgileCard.REVIEW_FEEDBACK,
        )
        self.review_feedback_project_card.assignees.add(self.assignee_user)
        self.review_feedback_project_card.reviewers.add(self.reviewer_user)

        self.in_progress_project_card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=models.ContentItem.PROJECT,
                project_submission_type=models.ContentItem.LINK,
            ),
            
            status=models.AgileCard.IN_PROGRESS,
        )
        self.in_progress_project_card.assignees.add(self.assignee_user)
        self.in_progress_project_card.reviewers.add(self.reviewer_user)

        self.ready_project_card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=models.ContentItem.PROJECT,
                project_submission_type=models.ContentItem.LINK,
            ),
            status=models.AgileCard.READY,
        )
        self.ready_project_card.assignees.add(self.assignee_user)
        self.ready_project_card.reviewers.add(self.reviewer_user)

        self.reviewable_cards = [
            self.in_review_project_card,
            self.complete_project_card,
            self.review_feedback_project_card,
        ]
    
    def test_superuser_can_add_review_on_reviewable_cards(self):
        for card in self.reviewable_cards:
            self.assertTrue(card.recruit_project.request_user_can_add_review(self.superuser))
    
    def test_users_can_review_complete_cards(self):
        self.assertTrue(self.complete_project_card.recruit_project.request_user_can_add_review(self.reviewer_user))
        self.assertTrue(self.complete_project_card.recruit_project.request_user_can_add_review(self.random_reviewer))
    
    def test_users_can_review_in_review_cards(self):
        self.assertTrue(self.in_review_project_card.recruit_project.request_user_can_add_review(self.reviewer_user))
    
    def test_users_can_review_review_feedback_cards(self):
        self.assertTrue(self.review_feedback_project_card.recruit_project.request_user_can_add_review(self.reviewer_user))
    
    def test_users_cannot_add_review_on_ip_cards(self):
        self.assertFalse(self.in_progress_project_card.recruit_project.request_user_can_add_review(self.reviewer_user))
        self.assertFalse(self.in_progress_project_card.recruit_project.request_user_can_add_review(self.superuser))
    
    def test_users_cannot_add_review_on_ready_cards(self):
        self.assertFalse(self.ready_project_card.recruit_project.request_user_can_add_review(self.reviewer_user))
        self.assertFalse(self.ready_project_card.recruit_project.request_user_can_add_review(self.superuser))
    
    def test_user_with_team_manage_permissions_can_add_review_on_reviewable_cards(self):
        for card in self.reviewable_cards:
            self.assertTrue(card.recruit_project.request_user_can_add_review(self.user_with_permissions))
    
    def test_user_with_team_manage_permissions_cannot_add_review_on_ip_r_cards(self):
        for card in [self.in_progress_project_card, self.ready_project_card]:
            self.assertFalse(card.recruit_project.request_user_can_add_review(self.user_with_permissions))


class positive_reviews_since_last_request_review_count_Tests(TestCase):
    def setUp(self):
        self.assignee_user = UserFactory()
        self.competent_reviewers = [UserFactory() for _ in range(2)]
        self.excellet_reviewer = UserFactory()
      
        self.in_review_project_card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=models.ContentItem.PROJECT,
                project_submission_type=models.ContentItem.LINK,
            ),
            status=models.AgileCard.IN_REVIEW,
        )

        self.in_review_project_card.assignees.add(self.assignee_user)
        self.in_review_project_card.reviewers.set([*self.competent_reviewers, self.excellet_reviewer])

        for reviewer in self.competent_reviewers:
            factories.RecruitProjectReviewFactory(
                reviewer_user=reviewer,
                status=COMPETENT,
                recruit_project=self.in_review_project_card.recruit_project,
                comments="Noice!",
            )

        factories.RecruitProjectReviewFactory(
            reviewer_user=self.excellet_reviewer,
            status=EXCELLENT,
            recruit_project=self.in_review_project_card.recruit_project,
            comments="Noicest!",
        )

    def test_positive_reviews_since_last_request_review_count(self):
        self.assertEqual(
            self.in_review_project_card.recruit_project.positive_reviews_since_last_request_review_count,
            3,
        )

