from django.core.management.base import BaseCommand
from core.models import User
from social_auth.models import SocialProfile
from config.models import NameSpace, Value
from curriculum_tracking.models import (
    AgileCard,
    CourseRegistration,
    ContentItem,
    ReviewTrust,
)
from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)
from core.models import Team, PERMISSION_VIEW_ALL
from guardian.shortcuts import assign_perm
from faker import Faker
from curriculum_tracking.card_generation_helpers import get_ordered_content_items

from curriculum_tracking.management.commands.import_curriculum import (
    save_curriculum_to_db,
)  # Note: these kinds of imports are actually bad practice. We need a refactor

from backend.settings import CURRICULUM_TRACKING_REVIEW_BOT_EMAIL


faker = Faker()


def _number_iter():
    i = 1
    while True:
        yield i
        i += 1


_numbers = _number_iter()


def make_github_name():
    name = f"test-github-user-{next(_numbers)}"
    print(name)
    return name


def create_user(email, github_name=None, is_staff=False, is_superuser=False):
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "is_staff": is_staff,
            "is_superuser": is_superuser,
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
        },
    )
    user.set_password(email)
    if github_name:
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


def setup_peer_reviewers(users):
    for user in users:
        peers = [u for u in users if u != user]

        cards = AgileCard.objects.filter(assignees__in=[user]).filter(
            content_item__content_type=ContentItem.PROJECT
        )

        for card in cards:
            card.reviewers.set(peers)
            card._create_project_progress_if_not_exists()
            card.recruit_project.reviewer_users.set(peers)


def create_team_of_learners(team_name, curriculum):
    team, _ = Team.objects.get_or_create(name=team_name)
    learners = [
        create_user(
            email=f"learner_{team_name.lower()}_{i+1}@email.com",
            github_name=make_github_name(),
        )
        for i in range(3)
    ]

    for user in learners:
        CourseRegistration.objects.get_or_create(user=user, curriculum=curriculum)
        AgileCard.objects.filter(assignees__in=[user]).delete()
        generate_and_update_all_cards_for_user(user, None)

        team.user_set.add(user)
        print(f"\ncreated learner user: {user.email}\n")

    setup_peer_reviewers(learners)

    for permission, _ in Team._meta.permissions:
        user = create_user(
            email=f"{permission.lower()}_{team_name.lower()}@email.com",
            github_name=make_github_name(),
            is_staff=True,
        )

        assign_perm(permission, user, team)

        print(f"\ncreated permission user: {user.email}\n")

    # create a JTL
    jtl_user = create_user(
        email=f"jtl_{team_name.lower()}@email.com",
        github_name=make_github_name(),
        is_staff=False,
    )
    assign_perm(PERMISSION_VIEW_ALL, jtl_user, team)
    print(f"\ncreated JTL user: {user.email}\n")


def create_challenge_users(count=10):
    for i in range(count):
        create_user(
            email=f"challenger_{i}@email.com",
        )


def add_bot_trust_to_projects_in_curriculum(curriculum):
    bot, _ = User.objects.get_or_create(email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL)
    for x in get_ordered_content_items(curriculum):
        content_item = x.content_item
        assert len(x.flavours) == 0, "TODO: this doesn't handle flavours for now"

        o, _ = ReviewTrust.objects.get_or_create(content_item=content_item, user=bot)
        # o.flavours.set(x.flavours)


class Command(BaseCommand):
    def handle(self, *args, **options):

        bot, _ = User.objects.get_or_create(email=CURRICULUM_TRACKING_REVIEW_BOT_EMAIL)

        # zmc challenge

        challenge = save_curriculum_to_db("dev_helpers/data/zmc-challenge-1.json")
        create_challenge_users()

        add_bot_trust_to_projects_in_curriculum(challenge)

        create_config_value(
            "curriculum_tracking/serializers/TeamStatsSerializer",
            "EXCLUDE_TAGS_FROM_REVIEW_STATS",
            "ncit",
            True,
            Value.STRING,
        )

        # frontend features

        curriculum = save_curriculum_to_db(
            "dev_helpers/data/intro-to-tilde-course.json"
        )

        create_user(
            email="super@email.com",
            github_name=make_github_name(),
            is_staff=True,
            is_superuser=True,
        )

        create_team_of_learners(team_name="A", curriculum=curriculum)
        create_team_of_learners(team_name="B", curriculum=curriculum)

        # bootcamp users
        bootcamp_curriculum = save_curriculum_to_db(
            "dev_helpers/data/web-dev-bootcamp-automarked.json"
        )

        create_team_of_learners(team_name="boot", curriculum=bootcamp_curriculum)
