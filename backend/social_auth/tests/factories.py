from factory.django import DjangoModelFactory
import factory
from core.tests.factories import UserFactory


def _github_name_generator():
    i = 1
    while True:
        yield f"gituser{i}"
        i += 1


_github_name_iterator = _github_name_generator()


class SocialProfileFactory(DjangoModelFactory):
    class Meta:
        model = "social_auth.SocialProfile"

    user = factory.SubFactory(UserFactory)
    github_name = factory.lazy_attribute(
        lambda *args, **kwargs: next(_github_name_iterator)
    )


class GithubOAuthTokenFactory(DjangoModelFactory):
    class Meta:
        model = "social_auth.GithubOAuthToken"

    user = factory.SubFactory(UserFactory)

    access_token = factory.Faker("first_name")
    token_type = "token"
    scope = factory.Faker("first_name")

