from factory.django import DjangoModelFactory
import factory
from core import models
from backend.settings import (
    AUTH_USER_MODEL,
)  # there's probably a cleaner way to import this.
from django.utils import timezone


def _email_generator():
    i = 1
    while True:
        yield f"foo.{i}@example.com"
        i += 1


def _group_name_generator():
    i = 1
    while True:
        yield f"GROUP NAME {i}"
        i += 1


_email_iterator = _email_generator()

_group_name_iterator = _group_name_generator()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = AUTH_USER_MODEL

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.lazy_attribute(lambda *args, **kwargs: next(_email_iterator))

    is_superuser = False
    is_staff = False


class UserGroupFactory(DjangoModelFactory):
    class Meta:
        model = "core.UserGroup"

    name = factory.lazy_attribute(lambda *args, **kwargs: next(_group_name_iterator))
    # kind = models.UserGroup.CLASS_ROOM


class UserGroupMembership(DjangoModelFactory):
    class Meta:
        model = "core.UserGroupMembership"

    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(UserGroupFactory)


class CurriculumFactory(DjangoModelFactory):
    class Meta:
        model = "core.Curriculum"

    short_name = factory.LazyAttribute(lambda o: o.name[:10])
    name = "hello"


class CohortFactory(DjangoModelFactory):
    class Meta:
        model = "core.Cohort"

    start_date = timezone.datetime.now()
    end_date = timezone.datetime.now()
    cohort_number = 15
    cohort_curriculum = factory.SubFactory(CurriculumFactory)
    label = "test"


class EmployerPartnerFactory(DjangoModelFactory):
    class Meta:
        model = "core.EmployerPartner"

    name = factory.Faker("company")


class RecruitCohortFactory(DjangoModelFactory):
    class Meta:
        model = "core.RecruitCohort"

    user = factory.SubFactory(UserFactory)
    cohort = factory.SubFactory(CohortFactory)
    employer_partner = factory.SubFactory(EmployerPartnerFactory)
    start_date = timezone.datetime.now()
    end_date = timezone.datetime.now()
