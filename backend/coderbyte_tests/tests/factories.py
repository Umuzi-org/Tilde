from factory.django import DjangoModelFactory
import factory
from coderbyte_tests.models import CoderbyteTestResult
from core.tests.factories import UserFactory


class CoderbyteTestResultFactory(DjangoModelFactory):
    class Meta:
        model = CoderbyteTestResult

    user = factory.SubFactory(UserFactory)
    report_link = factory.Faker("url")
    status = CoderbyteTestResult.STATUS_SUBMITTED
    date_joined = factory.Faker("date")
    date_invited = factory.Faker("date")
    assessment_name = "assessment_name"
    assessment_id = "assessment id"
    plagiarism = CoderbyteTestResult.PLAGIARISM_NOT_DETECTED
    time_taken_minutes = 30
    challenges_completed = 2
    challenge_score = 50
    multiple_choice_score = 50
    final_score = 50
