from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from . import factories
from core.models import Team
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group


# class TestUserViewSet(APITestCase, APITestCaseMixin):
#     LIST_URL_NAME = "user-list"
#     SUPPRESS_TEST_POST_TO_CREATE = True

#     def verbose_instance_factory(self):
#         user = factories.UserFactory()
#         return user


class TestUserStatsPermissions(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "user-list"
    SUPPRESS_TEST_GET_LIST = True
    SUPPRESS_TEST_POST_TO_CREATE = True

    def test_can_see_own_stats(self):
        user = factories.UserFactory()
        self.login(user)

        url = self.get_instance_url(pk=user.id) + "stats/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unpermissioned_users_get_permission_denied(self):
        user = factories.UserFactory()
        self.login(factories.UserFactory())

        url = self.get_instance_url(pk=user.id) + "stats/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_see_stats(self):
        user = factories.UserFactory()
        self.login(factories.UserFactory(is_superuser=True))

        url = self.get_instance_url(pk=user.id) + "stats/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_can_see_stats_if_has_view_access(self):
        user = factories.UserFactory()
        team = factories.TeamFactory()
        team.user_set.add(user)

        manager = factories.UserFactory()
        assign_perm(Team.PERMISSION_VIEW_ALL, manager, team)
        self.login(manager)

        url = self.get_instance_url(pk=user.id) + "stats/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


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


class TestBulkSetDueDatesApi(APITestCase, APITestCaseMixin):

    #LIST_URL_NAME = "managmentaction-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):

        team = factories.TeamFactory()
        user = factories.UserFactory()
        team.user_set.add(user)
        return team

    def setUp(self):

        #self.url = self.get_list_url()
        self.api_url = '/api/managment_actions/bulk_set_due_dates/'

        self.blue_team = factories.TeamFactory()
        self.red_team = factories.TeamFactory()
        self.user_one_blue = factories.UserFactory(first_name='one_blue', is_superuser=False, is_staff=False)
        self.user_two_blue = factories.UserFactory(first_name='two_blue', is_superuser=False, is_staff=False)
        self.user_one_red = factories.UserFactory(first_name='one_red', is_superuser=False, is_staff=False)
        self.user_two_red = factories.UserFactory(first_name='two_red', is_superuser=False, is_staff=False)

        self.blue_team.user_set.add(self.user_one_blue)
        self.blue_team.user_set.add(self.user_two_blue)
        self.red_team.user_set.add(self.user_one_red)
        self.red_team.user_set.add(self.user_two_red)

    def test_team_members_cannot_bulk_set_due_dates(self):

        self.login(self.user_one_blue)
        response = self.client.post(self.api_url)
        breakpoint()

