from django.test import TestCase

from core.admin import TeamAdmin


class TestModelAdminActionsExist(TestCase):
     def setUp(self) -> None:
          return super().setUp()

     def test_all_model_admin_actions_are_defined_for_team_admin(self):
          for admin_action in TeamAdmin.actions:
               self.assertIn(admin_action, dir(TeamAdmin))