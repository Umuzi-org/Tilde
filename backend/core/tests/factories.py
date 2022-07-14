from factory.django import DjangoModelFactory
import factory
from backend.settings import (
    AUTH_USER_MODEL,
)  # there's probably a cleaner way to import this.


def _email_generator():
    i = 1
    while True:
        yield f"foo.{i}@example.com"
        i += 1


def _team_name_generator():
    i = 1
    while True:
        yield f"GROUP NAME {i}"
        i += 1

def _organisation_name_generator():
    i = 1
    while True:
        yield f"GROUP NAME {i}"
        i += 1


_email_iterator = _email_generator()

_team_name_iterator = _team_name_generator()

_organisation_name_generator = _organisation_name_generator()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = AUTH_USER_MODEL

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.lazy_attribute(lambda *args, **kwargs: next(_email_iterator))

    is_superuser = False
    is_staff = False


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = "core.Team"

    name = factory.lazy_attribute(lambda *args, **kwargs: next(_team_name_iterator))
    active = True


class CurriculumFactory(DjangoModelFactory):
    class Meta:
        model = "core.Curriculum"

    name = "hello"



class StreamFactory(DjangoModelFactory):
    class Meta:
        model = "core.Stream"

    name = "Data Science"

class OrganisationFactory(DjangoModelFactory):
    class Meta:
        model = "core.Organisation"

    name = factory.lazy_attribute(lambda *args, **kwargs: next(_organisation_name_generator))


class StreamRegistrationFactory(DjangoModelFactory):
    class Meta:
        model = "core.StreamRegistration"

    user = factory.SubFactory(UserFactory)
    stream = factory.SubFactory(StreamFactory)
    employer_partner = factory.SubFactory(OrganisationFactory)
    name = 'C 20'
    start_date  = "2021-12-03"
    ideal_end_date = "2022-11-03"
    latest_end_date = "2022-12-03"     
    active = True