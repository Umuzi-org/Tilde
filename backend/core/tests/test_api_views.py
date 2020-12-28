from rest_framework.test import APITestCase
from test_mixins import APITestCaseMixin
from . import factories

class TestTeamViewSet(APITestCase, APITestCaseMixin):
    LIST_URL_NAME = "team-list"
    SUPPRESS_TEST_POST_TO_CREATE = True

    def verbose_instance_factory(self):
        membership = factories.TeamMembershipFactory()
        return membership.team

    # def test_only_returns_teams_i_can_see(self):   # ACL TODO
    #     user = factories.UserFactory(is_superuser=False)

    #     managed_team = factories.TeamFactory()
        
    #     #TODO

    #     self.login(user)
    #     url = self.get_list_url()

    #     response = self.client.get(url)
    #     self.assertEqual(response.data["count"], 2)

    #     ids = sorted([d["id"] for d in response.data["results"]])
    #     expected_ids = sorted([]) # TODO
    #     self.assertEqual(ids, expected_ids)

    def test_staff_users_see_all_teams(self):
        user = factories.UserFactory(is_superuser=False, is_staff=True)

        team = factories.TeamFactory()

        self.login(user)
        url = self.get_list_url()
        response = self.client.get(url)
        self.assertEqual(response.data["count"], 1)
        returned_id = response.data["results"][0]["id"]
        self.assertEqual(returned_id, team.id)
