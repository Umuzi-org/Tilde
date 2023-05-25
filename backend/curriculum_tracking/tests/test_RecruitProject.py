from core.tests.factories import TeamFactory, UserFactory
from django.test import TestCase

from curriculum_tracking import models
from curriculum_tracking.tests import factories
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
