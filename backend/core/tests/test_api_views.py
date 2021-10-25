from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from . import factories
from core.models import Team
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group


class TestTeamViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "team-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        team = factories.TeamFactory()
        user = factories.UserFactory()
        team.user_set.add(user)
        return team

    def test_only_returns_teams_i_can_see(self):

        url = self.get_list_url()
        super_user = factories.UserFactory(is_superuser=True)
        staff_user = factories.UserFactory(is_staff=True)
        normal_user = factories.UserFactory()

        team_1 = factories.TeamFactory()
        factories.TeamFactory()

        self.login(super_user)

        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)

        self.login(staff_user)

        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

        for permission, _ in Team._meta.permissions:
            # make sure that users can read what they need to
            user = factories.UserFactory()
            assign_perm(permission, user, team_1)
            self.login(user)

            response = self.client.get(url)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["id"], team_1.id)

            # check that it works for groups as well
            group = Group.objects.create(name=f"{permission} group")
            user = factories.UserFactory()
            group.user_set.add(user)
            assign_perm(permission, group, team_1)

            self.login(user)

            response = self.client.get(url)
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["id"], team_1.id)

        self.login(normal_user)

        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)

    def test_staff_users_cant_see_all_teams(self):
        user = factories.UserFactory(is_superuser=False, is_staff=True)

        factories.TeamFactory()

        self.login(user)
        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)
