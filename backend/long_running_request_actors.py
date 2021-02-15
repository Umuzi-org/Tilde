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


@dramatiq.actor(time_limit=10 * minute)
def team_shuffle_review_self(team_id, content_item_id):
    from curriculum_tracking.reviewer_allocation_helpers import team_shuffle_review_self

    team = Team.objects.get(pk=team_id)
    content_item = ContentItem.objects.get(pk=content_item_id)
    team_shuffle_review_self(team, content_item)


@dramatiq.actor(time_limit=10 * minute)
def team_shuffle_review_other():
    from curriculum_tracking.reviewer_allocation_helpers import (
        team_shuffle_review_other,
    )

    team_shuffle_review_other(reviewed_team, content_item, reviewer_team)


@dramatiq.actor(time_limit=10 * minute)
def bulk_add_user_as_card_reviewer():
    from curriculum_tracking.reviewer_allocation_helpers import (
        bulk_add_user_as_card_reviewer,
    )

    bulk_add_user_as_card_reviewer(team, content_item, reviewer_user)


@dramatiq.actor(time_limit=10 * minute)
def bulk_add_user_to_repo_only():
    from curriculum_tracking.reviewer_allocation_helpers import (
        bulk_add_user_to_repo_only,
    )

    bulk_add_user_to_repo_only(team, content_item, reviewer_user)
