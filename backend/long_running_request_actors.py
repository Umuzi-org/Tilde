"""
These are dramatiq actors

See https://dramatiq.io/guide.html
"""

import dramatiq
import os
import django

PRIORITY_LOW = 100
PRIORITY_MEDIUM = 50
PRIORITY_HIGH = 0


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
#### NB dont import any models until ADTER django.setup is called


from dramatiq.brokers.rabbitmq import RabbitmqBroker
from backend.settings import (
    RABBITMQ_USER,
    RABBITMQ_HOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
)

from social_auth.models import SocialProfile

connection = {}
if RABBITMQ_PASSWORD:
    connection[
        "url"
    ] = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}"

rabbitmq_broker = RabbitmqBroker(**connection)
dramatiq.set_broker(rabbitmq_broker)

MINUTE = 60 * 1000


@dramatiq.actor(time_limit=10 * MINUTE)
def test_long_running_request():

    from core.models import User

    count = User.objects.filter(active=True).count()
    print(f"Active users: {count}")


@dramatiq.actor()
def recruit_project_setup_repository(project_id):
    from curriculum_tracking.models import RecruitProject

    project = RecruitProject.objects.get(pk=project_id)
    project.setup_repository()


@dramatiq.actor()
def recruit_project_invite_github_collaborators_to_repo(project_id):
    from curriculum_tracking.models import RecruitProject

    project = RecruitProject.objects.get(pk=project_id)
    project.invite_github_collaborators_to_repo()


@dramatiq.actor()
def auto_assign_reviewers():
    from curriculum_tracking.management.auto_assign_reviewers import (
        auto_assign_reviewers as work,
    )

    work()


@dramatiq.actor()
def user_delete_and_recreate_cards(user_id):
    from core.models import User
    from curriculum_tracking import models
    from curriculum_tracking.card_generation_helpers import (
        generate_and_update_all_cards_for_user,
    )

    user = User.objects.get(pk=user_id)
    models.AgileCard.objects.filter(assignees__in=[user]).delete()
    generate_and_update_all_cards_for_user(user, None)
