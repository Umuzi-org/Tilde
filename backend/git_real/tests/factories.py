from factory.django import DjangoModelFactory
import factory
from django.utils import timezone


from core.tests.factories import UserFactory


def _repo_full_name_generator():
    i = 1
    while True:
        yield f"https://something.com/like_this{i}"
        i += 1


_repo_full_name_iterator = _repo_full_name_generator()
_repo_ssh_url_iterator = _repo_full_name_iterator


class RepositoryFactory(DjangoModelFactory):
    class Meta:
        model = "git_real.Repository"

    owner = factory.Faker("first_name")
    full_name = factory.LazyAttribute(
        lambda *args, **kwargs: next(_repo_full_name_iterator)
    )

    ssh_url = factory.LazyAttribute(
        lambda *args, **kwargs: next(_repo_ssh_url_iterator)
    )
    # ssh_url = factory.Faker("url")
    created_at = timezone.now()
    private = True
    archived = False

    user = factory.SubFactory(UserFactory)
