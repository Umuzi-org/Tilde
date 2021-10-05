from core.tests import factories
from django.test import TestCase
from core.admin import delete_all_inactive_teams
from core.admin import TeamAdmin
from django.http.request import HttpRequest
from mock import patch


class TestDeletingInactiveTeams(TestCase):

    @patch('django.db.models.query.QuerySet', return_value=[
        factories.TeamFactory(),
        factories.TeamFactory(),
        factories.TeamFactory()
    ])
    def test_delete_all_inactive_teams_should_not_delete_any_teams_as_all_teams_are_active(self, mocked_queryset):
        # Making sure the three teams created during the 'Mocking' process are all 'active'
        assert [team.active == True for team in mocked_queryset.return_value]
        delete_all_inactive_teams(TeamAdmin, HttpRequest, mocked_queryset.return_value)

        # Checking that no teams were deleted as they are all currently active
        assert len(mocked_queryset.return_value) == 3

    @patch('django.db.models.query.QuerySet', return_value=[
        factories.TeamFactory(),
        factories.TeamFactory(),
        factories.TeamFactory()
    ])
    def test_delete_all_inactive_teams_should_delete_the_one_team_which_will_be_made_inactive(self, mocked_queryset):
        # Changing the status of the 1st of the three teams to not active
        mocked_queryset.return_value[0].active = False
        assert mocked_queryset.return_value[0].active == False

        # Now calling delete_all_inactive_teams will delete the inactive team leaving only two teams
        results = delete_all_inactive_teams(TeamAdmin, HttpRequest, mocked_queryset.return_value)
        assert len(results) < 3
