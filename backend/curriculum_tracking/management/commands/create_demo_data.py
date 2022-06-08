from django.core.management.base import BaseCommand
from core.models import User
from social_auth.models import SocialProfile
from config.models import NameSpace,Value
from curriculum_tracking.models import AgileCard, CourseRegistration
from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)
from core.models import Team
from guardian.shortcuts import assign_perm


from curriculum_tracking.management.commands.import_curriculum import save_curriculum_to_db  # Note: these kinds of imports are actually bad practice. We need a refactor

def _number_iter():
    i=1
    while True:
        yield i
        i+=1

_numbers = _number_iter()


def make_github_name():
    name= f"test-github-user-{next(_numbers)}"
    print (name)
    return name

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



def create_team_of_learners(team_name,curriculum):
    team,_ = Team.objects.get_or_create(name=team_name)
    learners = [
            create_user(f"learner_{team_name.lower()}_{i+1}@email.com",make_github_name()) for i in range(3)
        ]

    for user in learners:
        CourseRegistration.objects.get_or_create(
            user=user, curriculum=curriculum
        )
        AgileCard.objects.filter(assignees__in=[user]).delete()
        generate_and_update_all_cards_for_user(user,None)

        team.user_set.add(user)
        print(f"\ncreated learner user: {user.email}\n")


    for permission,_ in Team._meta.permissions:
        user = create_user(f"{permission.lower()}_{team_name.lower()}@email.com",make_github_name(), True)

        assign_perm(permission, user, team)

        print(f"\ncreated permissioned user: {user.email}\n")


class Command(BaseCommand):
    def handle(self, *args, **options):

        create_config_value("curriculum_tracking/serializers/TeamStatsSerializer", "EXCLUDE_TAGS_FROM_REVIEW_STATS", "ncit", True, Value.STRING)

        curriculum = save_curriculum_to_db("dev_helpers/data/intro-to-tilde-course.json")


        create_user("super@email.com",make_github_name(),True,True)

        create_team_of_learners(team_name="A",curriculum=curriculum)
        create_team_of_learners(team_name="B",curriculum=curriculum)



