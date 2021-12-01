from django.test import TestCase
from core.tests.factories import TeamFactory, UserFactory
from curriculum_tracking.tests.factories import ProjectContentItemFactory, RecruitProjectFactory
from curriculum_tracking.management.commands.export_project_urls import get_user_and_projectlink


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
        project = RecruitProjectFactory(link_submission='https://i_am_a_link')
        link = project.link_submission
        user = project.recruit_users.first()
        team.users.add(user)

        result = get_user_and_projectlink(team, project.content_item)
        self.assertEqual(result[0], [user.email, link])

    def test_multiple_projects_submitted(self):
        team = TeamFactory()
        project1 = RecruitProjectFactory(link_submission='https://i_am_a_link')
        link1 = project1.link_submission
        user1 = project1.recruit_users.first()
        team.users.add(user1)

        project2 = RecruitProjectFactory(link_submission='https://i_am_another_link', content_item=project1.content_item)
        link2 = project2.link_submission
        user2 = project2.recruit_users.first()
        team.users.add(user2)

        results = get_user_and_projectlink(team, project1.content_item)
        self.assertEqual(results[0], [user1.email, link1])
        self.assertEqual(results[1], [user2.email, link2])
