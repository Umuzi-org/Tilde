from datetime import timedelta
from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone

from curriculum_tracking import models
from curriculum_tracking.tests import factories
from core.models import Team
from core.tests.factories import TeamFactory, UserFactory
from guardian.shortcuts import assign_perm
from activity_log.models import LogEntry
import curriculum_tracking.activity_log_entry_creators as log_creators


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


class get_total_duration(TestCase):

    def test_returns_none_when_there_are_no_log_entries(self):
        user = factories.UserFactory(is_superuser=False)
        card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=models.ContentItem.PROJECT, project_submission_type="L"
            ),
            status=models.AgileCard.READY,
        )

        card.assignees.set([user])
        card.start_project()
        self.assertIn("get_total_duration", dir(card.recruit_project))
        self.assertEquals(card.recruit_project.get_total_duration, None)

    def test_returns_correct_duration(self):
        user = factories.UserFactory(is_superuser=False)

        card = factories.AgileCardFactory(
            content_item=factories.ContentItemFactory(
                content_type=models.ContentItem.PROJECT, project_submission_type="L"
            ),
            status=models.AgileCard.READY,
        )

        card.assignees.set([user])
        card.start_project()

        with patch.object(
            LogEntry._meta.get_field("timestamp"), "auto_now_add", True
        ), patch(
            "django.utils.timezone.now",
            side_effect=[
                timezone.now(),
                timezone.now(),
                timezone.now(),
                timezone.now() + timedelta(hours=3),
            ],
        ):
            log_creators.log_card_started(card=card, actor_user=user)
            log_creators.log_card_moved_to_complete(card=card, actor_user=user)

            card.status = "C"

            self.assertEquals(
                card.recruit_project.get_total_duration, "0 days, 3 hours, 0 minutes"
            )
