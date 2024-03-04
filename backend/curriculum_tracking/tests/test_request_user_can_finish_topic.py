from django.test import TestCase
from guardian.shortcuts import assign_perm
from curriculum_tracking.models import AgileCard, ContentItem
from curriculum_tracking.tests import factories
from core.tests import factories as core_factories
from core.models import Team


class request_user_can_finish_topic_Tests(TestCase):
    def setUp(self):
        self.assignee_user = core_factories.UserFactory()
        self.superuser = core_factories.UserFactory(is_superuser=True)
        self.user_with_manage_permissions = core_factories.UserFactory()
        self.user_without_manage_permissions = core_factories.UserFactory()
        self.user_team = core_factories.TeamFactory()

        self.user_team.user_set.add(self.assignee_user)
        self.user_team.save()

        assign_perm(
            Team.PERMISSION_MANAGE_CARDS,
            self.user_with_manage_permissions,
            self.user_team,
        )


        self.topic_card = factories.AgileCardFactory(
            status=AgileCard.READY,
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.TOPIC
            ),
            recruit_project=None,
        )
        self.topic_card.assignees.set([self.assignee_user,])
        self.topic_card.start_topic()

        self.project_card: AgileCard = factories.AgileCardFactory(
            status=AgileCard.READY,
            content_item=factories.ContentItemFactory(
                content_type=ContentItem.PROJECT,
                project_submission_type=ContentItem.LINK,
            ),
            recruit_project=None,
        )
        self.project_card.assignees.set([self.assignee_user,])
        self.project_card.start_project()


    def test_assignee_can_finish_topic_on_ip_cards(self):
        self.assertTrue(
            self.topic_card.request_user_can_finish_topic(self.assignee_user)
        )

    def test_user_with_team_manage_permissions_can_finish_topic(self):
   
        self.assertTrue(
            self.topic_card.request_user_can_finish_topic(
                self.user_with_manage_permissions
            )
        )

    def test_superuser_can_finish_topic(self):
        self.assertTrue(self.topic_card.request_user_can_finish_topic(self.superuser))


    def test_user_without_team_manage_permissions_cannot_finish_topic(self):
        self.assertFalse(
            self.topic_card.request_user_can_finish_topic(
                self.user_without_manage_permissions
            )
        )
        
    def test_non_topic_card_cannot_be_finished(self):
        self.assertFalse(
            self.project_card.request_user_can_finish_topic(self.assignee_user)
        )
        self.assertFalse(
            self.project_card.request_user_can_finish_topic(
                self.user_with_manage_permissions
            )
        )
        self.assertFalse(
            self.project_card.request_user_can_finish_topic(self.superuser)
        )
        self.assertFalse(
            self.project_card.request_user_can_finish_topic(
                self.user_without_manage_permissions
            )
        )
