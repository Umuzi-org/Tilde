from django.db.models import manager
from django.test import TestCase
from core.tests.factories import UserFactory
from curriculum_tracking.tests.factories import TeamFactory
from guardian.shortcuts import assign_perm
from core.models import Team

# from django.contrib.auth.models import Group


class get_permissions_Tests(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.team = TeamFactory()

        self.managment_team = Team.objects.create(name="sasad")
        self.managment_team.user_set.add(self.user)

    def test_no_permissions(self):
        result = self.user.get_permissions()
        self.assertEqual(result, {"teams": {}})

    def test_direct_team_permissions(self):
        assign_perm(Team.PERMISSION_REVIEW_CARDS, self.user, self.team)
        assign_perm(Team.PERMISSION_MANAGE_CARDS, self.user, self.team)

        permissions = self.user.get_permissions()
        result = [t for t in permissions["teams"][self.team.id]["permissions"]]
        self.assertEqual(
            sorted(result),
            [
                Team.PERMISSION_MANAGE_CARDS,
                Team.PERMISSION_REVIEW_CARDS,
            ],
        )

    def test_group_team_permissions(self):
        assign_perm(Team.PERMISSION_REVIEW_CARDS, self.managment_team, self.team)
        assign_perm(Team.PERMISSION_MANAGE_CARDS, self.managment_team, self.team)
        # result = [t[0] for t in self.user.get_permissions()["teams"][self.team.id]]
        permissions = self.user.get_permissions()
        result = [t for t in permissions["teams"][self.team.id]["permissions"]]

        self.assertEqual(
            sorted(result),
            [
                Team.PERMISSION_MANAGE_CARDS,
                Team.PERMISSION_REVIEW_CARDS,
            ],
        )

    def test_permissions_work_for_auth_groups_and_teams(self):
        """we use Teams but django still uses a concept called Group, make sure that any way we add permissions syncs up between all the things"""

        managed_team = TeamFactory()

        manager_team = TeamFactory()
        manager_group = manager_team.group_ptr

        # add a user to the team, it should be in the group
        user = UserFactory()
        manager_team.user_set.add(user)
        self.assertEqual(list(manager_group.user_set.all()), [user])

        # give a permission to a group and the team should have it
        assign_perm(Team.PERMISSION_REVIEW_CARDS, manager_group, managed_team)
        assign_perm(Team.PERMISSION_MANAGE_CARDS, manager_team, managed_team)

        permissions = user.get_permissions()
        result = [t for t in permissions["teams"][managed_team.id]["permissions"]]

        self.assertEqual(
            sorted(result),
            [
                Team.PERMISSION_MANAGE_CARDS,
                Team.PERMISSION_REVIEW_CARDS,
            ],
        )


class has_perm_Tests(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=False)
        self.team = TeamFactory()

    def test_returns_correctly_when_assigning_permissions_to_users(self):

        self.assertEqual(
            self.user.has_perm(Team.PERMISSION_ASSIGN_REVIEWERS, self.team), False
        )
        self.assertEqual(
            self.user.has_perm(Team.PERMISSION_MANAGE_CARDS, self.team), False
        )

        assign_perm(Team.PERMISSION_MANAGE_CARDS, self.user, self.team)

        self.assertEqual(
            self.user.has_perm(Team.PERMISSION_ASSIGN_REVIEWERS, self.team), False
        )
        self.assertEqual(
            self.user.has_perm(Team.PERMISSION_MANAGE_CARDS, self.team), True
        )

    def test_returns_correctly_when_assigning_permissions_to_managing_team(self):

        managment_team = TeamFactory()
        managment_team.users.add(self.user)

        assign_perm(Team.PERMISSION_MANAGE_CARDS, managment_team, self.team)
        self.assertEqual(
            self.user.has_perm(Team.PERMISSION_ASSIGN_REVIEWERS, self.team), False
        )
        self.assertEqual(
            self.user.has_perm(Team.PERMISSION_MANAGE_CARDS, self.team), True
        )
