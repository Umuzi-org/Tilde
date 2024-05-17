from core.tests.factories import TeamFactory
from core.models import Team
from django.test import TestCase


class TestTeamSearch(TestCase):
    def test_get_teams_from_search_term(self):
        TeamFactory(name="boots 1999")
        TeamFactory(name="boots 2014")
        TeamFactory(name="detectives")

        teams_from_search_term = Team.get_teams_from_search_term("boots")

        self.assertEqual(len(teams_from_search_term), 2)

        teams_from_search_term = Team.get_teams_from_search_term("t")
        self.assertEqual(len(teams_from_search_term), 3)

        teams_from_search_term = Team.get_teams_from_search_term("zzzzzzzzz")
        self.assertEqual(len(teams_from_search_term), 0)

        teams_from_search_term = Team.get_teams_from_search_term("det")
        self.assertEqual(len(teams_from_search_term), 1)
        self.assertEqual(teams_from_search_term.first().name, "detectives")
