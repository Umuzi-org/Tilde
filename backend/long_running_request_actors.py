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


from dramatiq.brokers.rabbitmq import RabbitmqBroker
from backend.settings import (
    RABBITMQ_USER,
    RABBITMQ_HOST,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
)

connection = {}
if RABBITMQ_PASSWORD:
    connection[
        "url"
    ] = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}"

rabbitmq_broker = RabbitmqBroker(**connection)
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor(time_limit=60000)
def test_long_running_request():

    from core.models import User

    count = User.objects.filter(active=True).count()
    print(f"Active users: {count}")


@dramatiq.actor(time_limit=10 * 60 * 1000)
def team_shuffle_review_self(team_id, flavour_names, content_item_id):
    TODO


@dramatiq.actor()
def add_collaborator_and_protect_master(project_id):
    from social_auth.github_api import Api
    from git_real.constants import GITHUB_BOT_USERNAME
    from git_real.helpers import add_collaborator, protect_master
    from curriculum_tracking.models import RecruitProject
    from social_auth.github_api import Api

    api = Api(GITHUB_BOT_USERNAME)
    project = RecruitProject.objects.get(pk=project_id)
    repo = project.repository
    protect_master(api, repo.full_name)
    for user in project.reviewer_users.all():
        if user.active:
            add_collaborator(api, repo.full_name, user.social_profile.github_name)
    for user in project.recruit_users.all():
        if user.active:
            add_collaborator(api, repo.full_name, user.social_profile.github_name)
