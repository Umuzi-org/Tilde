from factory.django import DjangoModelFactory
from selection_bootcamps import models
import factory
from core.tests.factories import StreamFactory, TeamFactory
from django.utils import timezone


class EmptyBootcampFactory(DjangoModelFactory):
    class Meta:
        model = "selection_bootcamps.Bootcamp"

    stream = factory.SubFactory(StreamFactory)
    team = factory.SubFactory(TeamFactory)
    start_date = factory.LazyFunction(timezone.now)
    end_date = factory.LazyFunction(
        lambda: timezone.now() + timezone.timedelta(days=14)
    )
