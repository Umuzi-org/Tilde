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
        self.assertEqual(result[0], [user.email, None])

    def test_project_submitted(self):
        team = TeamFactory()
        project = factories.RecruitProjectFactory(link_submission='https://i_am_a_link')
        link = project.link_submission  # -> <Repository: https://something.com/like_this4>
        user = project.recruit_users.first()  # ->  <User: foo.5@example.com>
        team.users.add(user)

        result = get_user_and_projectlink(team, project.content_item)
        self.assertEqual(result[0], [user.email, link])

    def test_multiple_projects_submitted(self):
        team = TeamFactory()
        project1 = factories.RecruitProjectFactory(link_submission='https://i_am_a_link')
        link1 = project1.link_submission  # -> <Repository: https://something.com/like_this4>
        user1 = project1.recruit_users.first()  # ->  <User: foo.5@example.com>
        team.users.add(user1)

        project2 = factories.RecruitProjectFactory(link_submission='https://i_am_another_link', content_item=project1.content_item) # makes this the same project
        link2 = project2.link_submission
        user2 = project2.recruit_users.first()
        team.users.add(user2)

        results = get_user_and_projectlink(team, project1.content_item)
        self.assertEqual(results[0], [user1.email, link1])
        self.assertEqual(results[1], [user2.email, link2])
