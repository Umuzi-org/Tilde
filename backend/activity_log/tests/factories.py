from factory.django import DjangoModelFactory
import factory
from django.utils import timezone
from factory.helpers import lazy_attribute
from core.tests.factories import UserFactory


def _event_name_generator():
    i = 1
    while True:
        yield f"tag{i}"
        i += 1


_event_name_iterator = _event_name_generator()


class EventTypeFactory(DjangoModelFactory):
    class Meta:
        model = "activity_log.EventType"

    name = factory.LazyAttribute(lambda *args, **kwargs: next(_event_name_iterator))
    description = ""


class LogEntryFactory(DjangoModelFactory):
    class Meta:
        model = "activity_log.LogEntry"

    event_type = factory.SubFactory(EventTypeFactory)
    actor_user = factory.SubFactory(UserFactory)
    effected_user = factory.SubFactory(UserFactory)
