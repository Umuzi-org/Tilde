from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin

# from django.urls import reverse
from . import factories


class TestTeamViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "team-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        membership = factories.TeamMembership(permission_student=True)
        return membership.group

    def test_only_returns_groups_i_can_see(self):
        user = factories.UserFactory(is_superuser=False)

        managed_group = factories.TeamFactory()
        viewable_group = factories.TeamFactory()
        student_group = factories.TeamFactory()
        # nothing_group = factories.TeamFactory()

        factories.TeamMembership(
            user=user, group=student_group, permission_student=True
        )
        factories.TeamMembership(user=user, group=viewable_group, permission_view=True)
        factories.TeamMembership(user=user, group=managed_group, permission_manage=True)

        self.login(user)
        url = self.get_list_url()

        response = self.client.get(url)
        self.assertEqual(response.data["count"], 2)

        ids = sorted([d["id"] for d in response.data["results"]])
        expected_ids = sorted([managed_group.id, viewable_group.id])
        self.assertEqual(ids, expected_ids)

    def test_staff_users_see_all_groups(self):
        user = factories.UserFactory(is_superuser=False, is_staff=True)

        group = factories.TeamFactory()

        self.login(user)
        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(response.data["count"], 1)
        returned_id = response.data["results"][0]["id"]
        self.assertEqual(returned_id, group.id)
