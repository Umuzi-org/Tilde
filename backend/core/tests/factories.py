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

_email_iterator = _email_generator()



class UserFactory(DjangoModelFactory):
    class Meta:
        model = AUTH_USER_MODEL

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.lazy_attribute(lambda *args, **kwargs: next(_email_iterator))

    is_superuser = False
    is_staff = False


class CurriculumFactory(DjangoModelFactory):
    class Meta:
        model = "core.Curriculum"

    name = "hello"
