from django.test import TestCase
from core.tests.factories import TeamFactory, UserFactory
from guardian.shortcuts import assign_perm
from core.models import Team
from django.contrib.auth.models import Group


class get_permissions_Tests(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.team = TeamFactory()
        self.group = Group.objects.create(name="sasad")
        self.group.user_set.add(self.user)

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
        assign_perm(Team.PERMISSION_REVIEW_CARDS, self.group, self.team)
        assign_perm(Team.PERMISSION_MANAGE_CARDS, self.group, self.team)
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