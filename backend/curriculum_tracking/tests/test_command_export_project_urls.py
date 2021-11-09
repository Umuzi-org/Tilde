from core.tests.factories import TeamFactory, UserFactory
from curriculum_tracking.tests.factories import ProjectContentItemFactory, RecruitProjectFactory
from django.test import TestCase
from curriculum_tracking import models
from curriculum_tracking.management.commands.export_project_urls import get_user_and_projectlink

from curriculum_tracking.tests import factories
from git_real.tests import factories as git_real_factories


class TestCommandExportProject(TestCase):

    def test_project_not_submitted(self):
        team = TeamFactory()
        user = UserFactory()
        team.users.add(user)
        content_item = ProjectContentItemFactory()
        result = get_user_and_projectlink(team, content_item)
        self.assertEqual(result, [user.email, None])

    def test_project_submitted(self):
        team = TeamFactory()
        project = factories.RecruitProjectFactory(link_submission='https://i_am_a_link')
        content_item = project.content_item
        link = project.link_submission  # -> <Repository: https://something.com/like_this4>
        user = project.recruit_users.first()  # ->  <User: foo.5@example.com>
        team.users.add(user)

        result = get_user_and_projectlink(team, project.content_item)
        self.assertEqual(result, [user.email, link])

    def test_multiple_projects_submitted(self):
        
