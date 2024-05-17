from core.tests.factories import TeamFactory
from core.models import Team
from django.test import TestCase


class TeamSearchTestCase(TestCase):

    def setUp(self):
        self.boots_1999_team = TeamFactory(name="boots 1999", active=True)
        self.boots_2014_team = TeamFactory(name="boots 2014", active=True)
        self.detectives_team = TeamFactory(name="detectives", active=True)
        self.inactive_team = TeamFactory(name="inactive team", active=False)

    def test_search_term_detectives(self):
        search_term = "dEtecTivEs"
        teams = Team.get_teams_from_search_term(search_term)
        self.assertIn(self.detectives_team, teams)
        self.assertNotIn(self.boots_1999_team, teams)
        self.assertNotIn(self.boots_2014_team, teams)

    def test_search_term_boot(self):
        search_term = "BOOT"
        teams = Team.get_teams_from_search_term(search_term)
        self.assertIn(self.boots_1999_team, teams)
        self.assertIn(self.boots_2014_team, teams)
        self.assertNotIn(self.detectives_team, teams)

    def test_search_term_no_match(self):
        search_term = "zzzzzzzzzzz"
        teams = Team.get_teams_from_search_term(search_term)
        self.assertEqual(len(teams), 0)
