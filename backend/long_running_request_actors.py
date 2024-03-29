"""
These are dramatiq actors

See https://dramatiq.io/guide.html


# Retries

https://dramatiq.io/guide.html#message-retries

If retrying a task is especially expensive or weird, then make sure you configure retry behavior. Otherwise dramatiq might keep retrying things for as long as a month!
"""

import dramatiq
import os
import django

PRIORITY_LOW = 100
PRIORITY_MEDIUM = 50
PRIORITY_HIGH = 0


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
#### NB dont import any models until AFTER django.setup is called


# TODO:
# uses sys.exit(1) if there is a database error
# set default values
# @actor(max_age=3600000) # milliseconds
# set priorities for different things


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

MINUTE = 60 * 1000

from long_running_request_utils import actor


@actor(time_limit=10 * MINUTE)
def test_long_running_request():
    from core.models import User

    count = User.objects.filter(active=True).count()
    print(f"Active users: {count}")


@actor()
def test_kill_pod():
    raise django.db.utils.InterfaceError()


@actor()
def recruit_project_setup_repository(project_id):
    from curriculum_tracking.models import RecruitProject

    project = RecruitProject.objects.get(pk=project_id)
    project.setup_repository()


@actor()
def recruit_project_invite_github_collaborators_to_repo(project_id):
    from curriculum_tracking.models import RecruitProject

    project = RecruitProject.objects.get(pk=project_id)
    project.invite_github_collaborators_to_repo()


@actor(max_retries=3)
def invite_collaborators_for_team_projects(team_name, include_complete=False):
    from curriculum_tracking.models import RecruitProject

    projects_filter = {
        "recruit_users__groups__name": team_name,
    }
    if not include_complete:
        projects_filter["complete_time__isnull"] = True

    projects = RecruitProject.objects.filter(**projects_filter)

    for project in projects:
        recruit_project_invite_github_collaborators_to_repo.send(project.pk)


@actor()
def auto_assign_reviewers():
    # TODO should be a cron job, or Airflow DAG
    from curriculum_tracking.management.auto_assign_reviewers import (
        auto_assign_reviewers as work,
    )

    work()


@actor(max_retries=3)
def delete_and_recreate_user_cards(user_id):
    from curriculum_tracking.card_generation_helpers import (
        generate_and_update_all_cards_for_user,
    )
    from curriculum_tracking.models import AgileCard
    from core.models import User

    user = User.objects.get(pk=user_id)
    AgileCard.objects.filter(assignees__in=[user]).delete()
    generate_and_update_all_cards_for_user(user, None)


@actor(max_retries=3)
def bulk_regenerate_cards_for_team(team_id):
    from core.models import Team

    team = Team.objects.get(pk=team_id)
    for user in team.active_users:
        delete_and_recreate_user_cards.send(user.pk)


@actor()
def invite_user_to_github_org(user_id):
    from git_real.constants import GIT_REAL_BOT_USERNAME, ORGANISATION
    from social_auth.github_api import Api
    from core.models import User

    user = User.objects.get(pk=user_id)
    api = Api(GIT_REAL_BOT_USERNAME)
    api.add_user_to_org_return_accepted(
        organisation_name=ORGANISATION, github_name=user.github_name
    )


from automarker.long_running_request_actors import *
