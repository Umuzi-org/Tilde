from factory.declarations import LazyAttribute
from git_real.models import PullRequest, PullRequestReview
from factory.django import DjangoModelFactory
import factory
from django.utils import timezone


from core.tests.factories import UserFactory


def _repo_full_name_generator():
    i = 1
    while True:
        yield f"https://something.com/like_this{i}"
        i += 1


def _number_generator():
    i = 0
    while True:
        yield i
        i += 1


def _html_url_generator():
    i = 1
    while True:
        yield f"https://somewhere_html.com/like_this{i}"
        i += 1


def _commit_id_generator():
    i = 1
    while True:
        yield f"{i}21747298a3790fde1710f3aa2d03b55020575aa"
        i += 1


_repo_full_name_iterator = _repo_full_name_generator()
_repo_ssh_url_iterator = _repo_full_name_iterator
_number_iterator = _number_generator()
_html_url_generator = _html_url_generator()
_commit_id_generator = _commit_id_generator()


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


class PullRequestFactory(DjangoModelFactory):
    class Meta:
        model = "git_real.PullRequest"

    repository = factory.SubFactory(RepositoryFactory)
    created_at = factory.LazyAttribute(lambda *args, **kwargs: timezone.now())
    updated_at = factory.LazyAttribute(lambda *args, **kwargs: timezone.now())
    number = LazyAttribute(lambda *args, **kwargs: next(_number_iterator))

    title = "title"
    body = "body"
    state = PullRequest.OPEN


class PullRequestReviewFactory(DjangoModelFactory):
    class Meta:
        model = PullRequestReview

    html_url = factory.lazy_attribute(lambda *args, **kwargs: next(_html_url_generator))
    pull_request = factory.SubFactory(PullRequestFactory)
    author_github_name = factory.Faker("first_name")
    submitted_at = factory.lazy_attribute(lambda o: timezone.now())
    body = "A horse walks into a bar, the barman says 'Why the long face?'"
    state = "closed"
    commit_id = factory.LazyAttribute(lambda *args, **kwargs: next(_commit_id_generator))
