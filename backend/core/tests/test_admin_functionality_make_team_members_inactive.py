from core.tests import factories
from django.test import TestCase
from core.admin import deactivate_team_members
from mock import patch


class TestMakeTeamMembersInactiveForInactiveTeams(TestCase):

    def setUp(self):
        self.active_team = factories.TeamFactory()
        self.inactive_team = factories.TeamFactory(active=False)
        self.user = factories.UserFactory()
        self.active_team.users.add(self.user)
        self.inactive_team.users.add(self.user)

    @patch('core.admin.TeamAdmin')
    @patch('django.http.HttpRequest')
    def test_make_all_members_inactive_for_an_active_team(self, mocked_Request, mocked_Team):

        # Making sure the team is active and so to it's member
        assert self.active_team.active == True
        assert self.active_team.active_users[0].active == True
        deactivate_team_members(mocked_Team, mocked_Request, [self.active_team])

        # Checking that the team is still active but the member not
        assert self.active_team.active == True
        assert len(self.active_team.user_set.filter(active=False).all()) == 1
        assert self.user in self.active_team.user_set.filter(active=False).all()

    @patch('core.admin.TeamAdmin')
    @patch('django.http.HttpRequest')
    def test_make_all_members_inactive_for_an_inactive_team(self, mocked_Request, mocked_Team):

        # Making sure the team is inactive but it's team member is active
        assert self.inactive_team.active == False
        assert self.inactive_team.active_users[0].active == True
        deactivate_team_members(mocked_Team, mocked_Request, [self.inactive_team])

        # Checking that the team is still inactive and so to it's member
        assert self.inactive_team.active == False
        assert len(self.inactive_team.user_set.filter(active=False).all()) == 1
        assert self.user in self.inactive_team.user_set.filter(active=False).all()