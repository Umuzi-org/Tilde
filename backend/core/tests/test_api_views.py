from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from . import factories
from core.models import Team
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group
import mock
import long_running_request_actors


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

class Test_learner_delete_and_recreate_cards(APITestCase, APITestCaseMixin):
    LIST_URL_NAME="user-list"
    SUPPRESS_TEST_POST_TO_CREATE=True
    SUPPRESS_TEST_GET_LIST=True

    # @mock.patch('curriculum_tracking.api_views.Response')
    @mock.patch.object(long_running_request_actors.user_delete_and_recreate_cards, 'send')
    def test_send_called_from_api_view_action_option(self, send):
        # Response.return_value = HttpResponse({"status": "OK"})
        user = factories.UserFactory()
        superuser = factories.UserFactory(is_superuser=True)
        self.login(superuser)
        url = self.get_instance_url(pk=user.id) + "delete_and_recreate_cards/"
        response = self.client.post(url)
        send.assert_called()

    # @mock.patch.object("generate_and_update_all_cards_for_user")