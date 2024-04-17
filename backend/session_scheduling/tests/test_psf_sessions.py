from .base import TechnicalSessionTestCase
from core.tests.factories import UserFactory

from session_scheduling.management.commands.create_problem_solving_foundation_sessions import (
    get_most_recent_test_results,
)
from datetime import date, timedelta
from coderbyte_tests.tests.factories import CoderbyteTestResultFactory


class get_most_recent_test_results_TestCase(TechnicalSessionTestCase):
    def test_no_results(self):

        result = get_most_recent_test_results()
        self.assertEqual(list(result), [])

    def test_one_result_per_user(self):
        expected = []
        for _ in range(3):
            expected.append(
                CoderbyteTestResultFactory(assessment_name="Problem solving 5").id
            )

        result = get_most_recent_test_results()
        result = sorted([o.id for o in result])

        self.assertEqual(sorted(result), sorted(expected))

    def test_multiple_tests_per_user(self):
        expected = []
        today = date.today()

        for _ in range(3):
            user = UserFactory()

            latest = None
            for n in range(3):
                latest = (
                    latest
                    or CoderbyteTestResultFactory(
                        user=user,
                        assessment_name="Problem solving 5",
                        date_joined=today - timedelta(days=n + 1),
                    ).id
                )
            CoderbyteTestResultFactory(
                user=user, assessment_name="NOT PSF", date_joined=today
            )
            expected.append(latest)

        result = get_most_recent_test_results()
        result = sorted([o.id for o in result])
        self.assertEqual(sorted(result), sorted(expected))
