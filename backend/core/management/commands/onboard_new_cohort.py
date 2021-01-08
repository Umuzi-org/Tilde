"""
This script gets run after a bunch of people get accepted from a bootcamp. They get some umuzi email addresses, rocketchat users, etc
"""

from django.core.management.base import BaseCommand
import pandas as pd
from django.contrib.auth import get_user_model
from core.models import UserGroup
from ..rocketchat import Rocketchat, GROUP

OLD_EMAIL = "Old Email"
NEW_EMAIL = "New Email"
TEAM_NAME = "Team"


User = get_user_model()


def update_user_email(row):
    try:
        user = User.objects.get(email=row[OLD_EMAIL])
    except User.DoesNotExist:
        user = User.objects.get(email=row[NEW_EMAIL])

    user.email = row[NEW_EMAIL]
    user.save()


def add_user_to_group(row):
    team, _ = UserGroup.objects.get_or_create(name=row[TEAM_NAME])
    user = User.objects.get(email=row[NEW_EMAIL])
    team.users.add(user)


def create_rocketchat_user_and_add_to_channel(client, managment_usernames):
    managment_user_ids = [
        client.get_existing_user(username=username).user_id
        for username in managment_usernames
    ]

    def _create_rocketchat_user_and_add_to_channel(row):

        username = row[NEW_EMAIL].split("@")[0]
        name = " ".join([s.capitalize() for s in username.split(".")])
        channel_name = row[TEAM_NAME].replace(" ", "-").lower()

        user = client.create_user_if_not_exists(
            name=name, username=username, email=row[NEW_EMAIL], password=row[NEW_EMAIL]
        )

        channel = client.create_channel_if_not_exists(
            name=channel_name,
            channel_type=GROUP,
        )

        client.add_user_to_channnel(user.user_id, channel.channel_id)

        for user_id in managment_user_ids:
            client.add_user_to_channnel(user_id, channel.channel_id)

    return _create_rocketchat_user_and_add_to_channel


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path", type=str)
        parser.add_argument("rocketchat_user", type=str)
        parser.add_argument("rocketchat_pass", type=str)

    def handle(self, *args, **options):
        path = options["path"]
        rocketchat_user = options["rocketchat_user"]
        rocketchat_pass = options["rocketchat_pass"]

        df = pd.read_csv(path)

        # df.apply(update_user_email, axis=1)
        # df.apply(add_user_to_group, axis=1)

        client = Rocketchat()
        client.login(rocketchat_user, rocketchat_pass)
        try:
            df.apply(
                create_rocketchat_user_and_add_to_channel(
                    client, ["ryan", "asanda", "sheena"]
                ),
                axis=1,
            )
        except:
            import traceback

            print(traceback.format_exc())
        finally:
            client.logout()