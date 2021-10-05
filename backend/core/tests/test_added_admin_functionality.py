import core.admin
from core.tests import factories
from django.test import TestCase
from core.admin import delete_all_inactive_teams
from core.admin import TeamAdmin
from django.http.request import HttpRequest
from mock import patch


class TestDeletingInactiveTeams(TestCase):

    # Create three teams, all with an active status
    def setUp(cls):
        cls.team_one = factories.TeamFactory()
        cls.team_two = factories.TeamFactory()
        cls.team_three = factories.TeamFactory()

    @patch('core.admin.delete_all_inactive_teams', return_value=[
        "cls.team_one",
        "cls.team_two",
        "cls.team_three"
    ])
    def test_delete_all_inactive_teams_should_not_delete_any_teams_as_all_teams_are_active(cls, mocked_function):
        assert cls.team_two.active == True
        assert cls.team_three.active == True
        assert cls.team_one.active == True
        delete_all_inactive_teams(TeamAdmin, HttpRequest, mocked_function.return_value)
        breakpoint()