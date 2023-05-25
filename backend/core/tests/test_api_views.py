from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from . import factories
from core.models import Team
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group

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

