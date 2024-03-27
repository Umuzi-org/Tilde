from django.test import TestCase
from session_scheduling.management.commands.initialise_session_types import (
    initialise_session_types,
)
from session_scheduling.management.commands.create_bootcamp_sessions import (
    create_bootcamp_sessions,
)
from session_scheduling.models import Session
from selection_bootcamps.tests.factories import EmptyBootcampFactory


class TechnicalSessionTestCase(TestCase):
    def setUp(self):
        super().setUp()
        initialise_session_types()


class create_bootcamp_sessions_Tests(TechnicalSessionTestCase):
    def test_no_bootcamps(self):
        # nothing should happen
        create_bootcamp_sessions()
        self.assertEqual(len(Session.objects.all()), 0)

    def test_bootcamp_with_no_members(self):
        bootcamp = EmptyBootcampFactory()
        create_bootcamp_sessions()
        self.assertEqual(len(Session.objects.all()), 0)

    def test_bootcamp_with_members_no_completions(self):
        bootcamp = EmptyBootcampFactory()
        add_users
        create_bootcamp_sessions()
        self.assertEqual(len(Session.objects.all()), 0)

    def test_bootcamp_with_completed_cards(self):
        bootcamp = EmptyBootcampFactory()
        add_users
        create_bootcamp_sessions()
        self.assertEqual(len(Session.objects.all()), todo)
        assert correct

    def test_bootcamp_with_completed_cards_twice(self):
        bootcamp = EmptyBootcampFactory()
        add_users
        create_bootcamp_sessions()
        create_bootcamp_sessions()  # call it twice
        self.assertEqual(len(Session.objects.all()), todo)
        assert correct
