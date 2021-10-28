# from core.tests import factories
from core.tests.factories import TeamFactory, UserFactory
from curriculum_tracking.tests.factories import ContentItemFactory, ProjectContentItemFactory
from django.test import TestCase
from curriculum_tracking import models
from curriculum_tracking.management.commands.export_project_urls import get_email_and_url

class TestCommandExportProject(TestCase):

    def test_project_not_submitted(self):
        self.team = TeamFactory()
        self.user = UserFactory()
        self.team.users.add(self.user)

        card = ProjectContentItemFactory()
        result = get_email_and_url(self.team)
        self.assertEqual(result, [self.user.email, None])
