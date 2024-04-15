from django.test import TestCase
from coderbyte_tests.management.commands.pull_latest_coderbyte_data import (
    _get_minutes_or_none,
    _save_single_result,
)

# from django.contrib.auth import get_user_model
from coderbyte_tests.models import CoderbyteTestResult

from core.tests.factories import UserFactory
import datetime

# User = get_user_model()


class get_minutes_or_none_TestCase(TestCase):
    def test__get_minutes_or_none_20m(self):
        input = "20m"
        expected = 20
        result = _get_minutes_or_none(input)
        self.assertEqual(result, expected)

    def test__get_minutes_or_none_2h_20m(self):
        input = "2h 20m"
        expected = 140
        result = _get_minutes_or_none(input)
        self.assertEqual(result, expected)

    def test__get_minutes_or_none_2h(self):
        input = "2h"
        expected = 120
        result = _get_minutes_or_none(input)
        self.assertEqual(result, expected)

    def test__get_minutes_or_none_2m(self):
        input = "2m"
        expected = 2
        result = _get_minutes_or_none(input)
        self.assertEqual(result, expected)


class save_single_result_TestCase(TestCase):
    def test__save_single_result_no_user(self):
        result_row = {
            "Name": "foo.bar@umuzi",
            "Email": "foo.bar@umuzi.org",
            "Status": "Submitted",
            "Date Joined": "04/12/24",
            "Date Invited": "N/A",
            "Invited By": "lerato.mabe@umuzi.org",
            "Time Taken": "20m",
            "Challenges Completed": "2",
            "Challenge Score": "95",
            "Multiple Choice Score": "N/A",
            "Final Score": "95",
            "Plagiarism": "Likely",
            "Assessment ID": "software-engine-uy5ishc13z",
            "Assessment Name": "Problem solving 2.2",
            "Action": "N/A",
            "Report Link": "https://coderbyte.com/report/user04k9726jv:software-engine-uy5ishc13z",
        }
        _save_single_result(result_row)

        self.assertEqual(CoderbyteTestResult.objects.count(), 0)

    def test__save_single_result_with_user(self):
        user = UserFactory()

        result_row = {
            "Name": user.email,
            "Email": user.email,
            "Status": "Submitted",
            "Date Joined": "04/12/24",
            "Date Invited": "N/A",
            "Invited By": "lerato.mabe@umuzi.org",
            "Time Taken": "20m",
            "Challenges Completed": "2",
            "Challenge Score": "95",
            "Multiple Choice Score": "N/A",
            "Final Score": "95",
            "Plagiarism": "Likely",
            "Assessment ID": "software-engine-uy5ishc13z",
            "Assessment Name": "Problem solving 2.2",
            "Action": "N/A",
            "Report Link": "https://coderbyte.com/report/user04k9726jv:software-engine-uy5ishc13z",
        }
        _save_single_result(result_row)

        self.assertEqual(CoderbyteTestResult.objects.count(), 1)
        result = CoderbyteTestResult.objects.first()
        self.assertEqual(result.user, user)
        self.assertEqual(result.report_link, result_row["Report Link"])
        self.assertEqual(result.status, result_row["Status"])
        self.assertEqual(result.date_joined, datetime.date(2024, 4, 12))
        self.assertEqual(result.date_invited, None)
        self.assertEqual(result.time_taken_minutes, 20)
        self.assertEqual(result.challenges_completed, 2)
        self.assertEqual(result.challenge_score, 95)
        self.assertEqual(result.multiple_choice_score, None)
        self.assertEqual(result.final_score, 95)
        self.assertEqual(result.plagiarism, "Likely")
        self.assertEqual(result.assessment_name, result_row["Assessment Name"])
        self.assertEqual(result.assessment_id, result_row["Assessment ID"])

    def test_overwrite_existing_entry(self):
        user = UserFactory()
        result = CoderbyteTestResult.objects.create(
            user=user,
            report_link="https://coderbyte.com/report/user04k9726jv:software-engine-uy5ishc13z",
        )

        result_row = {
            "Name": user.email,
            "Email": user.email,
            "Status": "Submitted",
            "Date Joined": "04/12/24",
            "Date Invited": "N/A",
            "Invited By": "lerato.mabe@umuzi.org",
            "Time Taken": "20m",
            "Challenges Completed": "2",
            "Challenge Score": "95",
            "Multiple Choice Score": "N/A",
            "Final Score": "95",
            "Plagiarism": "Likely",
            "Assessment ID": "software-engine-uy5ishc13z",
            "Assessment Name": "Problem solving 2.2",
            "Action": "N/A",
            "Report Link": result.report_link,
        }

        self.assertEqual(CoderbyteTestResult.objects.count(), 1)

        _save_single_result(result_row)

        # still only one entry
        self.assertEqual(CoderbyteTestResult.objects.count(), 1)

        result.refresh_from_db()
        self.assertEqual(result.user, user)
        self.assertEqual(result.report_link, result_row["Report Link"])
        self.assertEqual(result.status, result_row["Status"])
        self.assertEqual(result.date_joined, datetime.date(2024, 4, 12))
        self.assertEqual(result.date_invited, None)
        self.assertEqual(result.time_taken_minutes, 20)
        self.assertEqual(result.challenges_completed, 2)
        self.assertEqual(result.challenge_score, 95)
        self.assertEqual(result.multiple_choice_score, None)
        self.assertEqual(result.final_score, 95)
        self.assertEqual(result.plagiarism, "Likely")
        self.assertEqual(result.assessment_name, result_row["Assessment Name"])
        self.assertEqual(result.assessment_id, result_row["Assessment ID"])
