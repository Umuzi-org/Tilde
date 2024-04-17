from django.test import TestCase

from session_scheduling.management.commands.initialise_session_types import (
    initialise_session_types,
)


class TechnicalSessionTestCase(TestCase):
    def setUp(self):
        super().setUp()
        initialise_session_types()
