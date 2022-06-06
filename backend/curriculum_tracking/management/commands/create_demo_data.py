from django.core.management.base import BaseCommand
from core.models import User
from social_auth.models import SocialProfile
from config.models import NameSpace,Value


def make_github_name(number):
    return f"test-github-user-{number}"

def create_user(email,github_name,is_staff=False,is_superuser=False ):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "is_staff": is_staff,
            "is_superuser": is_superuser,
        },

    )
    user.set_password(email)
    social_profile, created = SocialProfile.objects.get_or_create(
            user=user, defaults={"github_name": github_name}
        )
    user.save()

    return user


def create_config_value(
    namespace_name,
    value_name,
    value_value,
    value_repeated,
    value_datatype,
):
    namespace, _ = NameSpace.objects.get_or_create(
            name=namespace_name, defaults={"description": ""}
        )
    defaults = {
        "value": value_value,
        "repeated": value_repeated,
        "datatype": value_datatype,
    }

    Value.get_or_create_or_update(
        namespace=namespace,
        name=value_name,
        defaults=defaults,
        overrides=defaults,
    )



class Command(BaseCommand):
    def handle(self, *args, **options):

        create_config_value("curriculum_tracking/serializers/TeamStatsSerializer", "EXCLUDE_TAGS_FROM_REVIEW_STATS", "ncit", True, Value.STRING)

        create_user("super@email.com",make_github_name(1),True,True)
        create_user("manager@email.com",make_github_name(2),True)
        create_user("learner1@email.com",make_github_name(3))



