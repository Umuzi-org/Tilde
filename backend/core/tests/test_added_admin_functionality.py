from core.tests import factories
from django.test import TestCase
from core.admin import make_members_inactive_for_inactive_teams
from core.admin import TeamAdmin
from django.http.request import HttpRequest
from mock import patch


class TestMakeTeamMembersInactiveForInactiveTeams(TestCase):

    @patch('django.db.models.query.QuerySet', return_value=[
        factories.TeamFactory()
    ])
    def test_make_members_inactive_for_inactive_teams_should_not_make_any_members_inactive_since_team_is_active(
            self, mocked_queryset
    ):
        # Making sure the three teams created during the 'Mocking' process are all 'active'
        assert [team.active == True for team in mocked_queryset.return_value]
        make_members_inactive_for_inactive_teams(TeamAdmin, HttpRequest, mocked_queryset.return_value)

        # Checking that team is still active and not deleted and that no members from the team was made 'inactive'
        assert [team.active == True for team in mocked_queryset.return_value]
        assert mocked_queryset.return_value[0].active == True

    @patch('django.db.models.query.QuerySet', return_value=[
        factories.TeamFactory(active=False)
    ])
    def test_make_members_inactive_for_inactive_teams_should_make_all_members_inactive_of_inactive_team(
            self, mocked_queryset
    ):
        # Making sure the team is inactive
        assert mocked_queryset.return_value[0].active == False
        assert mocked_queryset.return_value[0].active_users != None

        # Now calling make_members_inactive_for_inactive_teams will make all members in the team inactive
        assert len(mocked_queryset.return_value[0].active_users) == 0
