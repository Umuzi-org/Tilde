from session_scheduling.management.commands.create_bootcamp_sessions import (
    create_bootcamp_sessions,
    bootcamp_project_content_item_ids,
    SESSION_BOOTCAMP_ASSESSMENT,
)
from session_scheduling.models import Session
from selection_bootcamps.tests.factories import EmptyBootcampFactory
from core.tests.factories import UserFactory, StreamFactory
from curriculum_tracking.tests.factories import (
    ContentItemFactory,
    RecruitProjectFactory,
)
from curriculum_tracking.models import RecruitProject
from django.utils import timezone

from .base import TechnicalSessionTestCase


class create_bootcamp_sessions_Tests(TechnicalSessionTestCase):
    def test_no_bootcamps(self):
        create_bootcamp_sessions()
        self.assertEqual(len(Session.objects.all()), 0)

    def test_bootcamp_with_no_members(self):
        bootcamp = EmptyBootcampFactory()
        create_bootcamp_sessions()
        self.assertEqual(len(Session.objects.all()), 0)

    def _add_users(self, bootcamp):
        team = bootcamp.team
        users = []
        for _ in range(3):
            user = UserFactory()
            users.append(user)
            team.users.add(user)
        return users

    def _create_content_items(self):
        for content_item_id in bootcamp_project_content_item_ids:
            ContentItemFactory(id=content_item_id)

    def _add_bootcamp_projects(self, user):
        for content_item_id in bootcamp_project_content_item_ids:
            project = RecruitProjectFactory(
                content_item_id=content_item_id,
                recruit_users=[user],
                complete_time=None,
            )
            assert project.complete_time == None

    def _complete_user_projects(self, user):
        for project in RecruitProject.objects.filter(recruit_users=user):
            project.complete_time = timezone.now()
            project.save()

    def test_bootcamp_with_members_no_completions(self):
        bootcamp = EmptyBootcampFactory()
        self._add_users(bootcamp=bootcamp)
        create_bootcamp_sessions()
        self.assertEqual(len(Session.objects.all()), 0)

    def test_bootcamp_with_completed_cards(self):
        JS = "javascript"
        stream = StreamFactory(flavours=[JS])
        assert stream.flavour_names == [JS]

        bootcamp = EmptyBootcampFactory(stream=stream)

        users = self._add_users(bootcamp=bootcamp)
        self._create_content_items()
        for user in users:
            self._add_bootcamp_projects(user)

        self._complete_user_projects(users[0])

        create_bootcamp_sessions()

        sessions = list(Session.objects.all())
        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertEqual(session.session_type.name, SESSION_BOOTCAMP_ASSESSMENT)
        self.assertEqual(session.flavour_names, [JS])
        self.assertEqual(session.related_object, bootcamp)
        self.assertIsNotNone(session.due_date)
        self.assertEqual(list(session.attendees.all()), [users[0]])

        self._complete_user_projects(users[1])
        create_bootcamp_sessions()

        sessions = list(Session.objects.all())
        self.assertEqual(len(sessions), 2)
        session = sessions[1]
        self.assertEqual(session.session_type.name, SESSION_BOOTCAMP_ASSESSMENT)
        self.assertEqual(session.flavour_names, [JS])
        self.assertEqual(session.related_object, bootcamp)
        self.assertIsNotNone(session.due_date)
        self.assertEqual(list(session.attendees.all()), [users[1]])

        self._complete_user_projects(users[2])
        create_bootcamp_sessions()

        sessions = list(Session.objects.all())
        self.assertEqual(len(sessions), 3)
        session = sessions[2]
        self.assertEqual(session.session_type.name, SESSION_BOOTCAMP_ASSESSMENT)
        self.assertEqual(session.flavour_names, [JS])
        self.assertEqual(session.related_object, bootcamp)
        self.assertIsNotNone(session.due_date)
        self.assertEqual(list(session.attendees.all()), [users[2]])

    def test_cancelled_sessions_get_rescheduled(self):
        JS = "javascript"
        stream = StreamFactory(flavours=[JS])
        assert stream.flavour_names == [JS]

        bootcamp = EmptyBootcampFactory(stream=stream)

        users = self._add_users(bootcamp=bootcamp)
        self._create_content_items()
        for user in users:
            self._add_bootcamp_projects(user)
            self._complete_user_projects(user)

        create_bootcamp_sessions()

        Session.objects.all().update(is_cancelled=True)

        create_bootcamp_sessions()

        sessions = list(Session.objects.all())
        self.assertEqual(len(sessions), 6)
