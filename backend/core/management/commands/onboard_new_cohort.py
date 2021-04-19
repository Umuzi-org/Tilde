"""
This script gets run after a bunch of people get accepted from a bootcamp. They get some umuzi email addresses, rocketchat users, etc
"""

from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Team
from ..rocketchat import Rocketchat, GROUP
from core.models import User
from google_helpers.utils import fetch_sheet
from curriculum_tracking.models import Curriculum, CourseRegistration
import os

OLD_EMAIL = "Old Email"
NEW_EMAIL = "New Email"
TEAM_NAME = "Team"
DEPARTMENT = "department"
BROKEN = "broken"


COURSES_BY_DEPARTMENT = {
    "web dev": [
        "Web development boot camp",
        "Post Bootcamp Soft Skills",
        "NCIT - JavaScript",
        "Web Development - part 1",
        "Web Development - part 2",
    ],
    "web dev alumni": [
        "Alumni Web developement Bootcamp",
        "Post Bootcamp Soft Skills",
        "Web Development - part 2",
    ],
    "data eng": [
        "Data Engineering boot camp",
        "Post Bootcamp Soft Skills",
        "NCIT - Python",
        "Data Engineering - part 1",
        "Data Engineering - part 2",
    ],
    "data eng alumni": [
        "Alumni Data Engineering Bootcamp",
        "Post Bootcamp Soft Skills",
        "Data Engineering - part 2",
    ],
    "java": [
        "Java boot camp",
        "Post Bootcamp Soft Skills",
        "NCIT - Java",
        "Java Systems Development - part 1",
        "Java Systems Development - part 2",
    ],
    "java alumni": [
        "Alumni Java Bootcamp",
        "Post Bootcamp Soft Skills",
        "Java Systems Development - part 2",
    ],
    "it support": [
        "Post Bootcamp Soft Skills",
        "IT Support and IT automation",
    ],
    "data sci": [
        "Data Science boot camp",
        "Post Bootcamp Soft Skills",
        "NCIT - Python",
        "Data Science",
    ],
}


def update_user_email(row):
    print(row)
    try:
        user = User.objects.get(email=row[OLD_EMAIL])
    except User.DoesNotExist:
        user = User.objects.get(email=row[NEW_EMAIL])

    user.email = row[NEW_EMAIL]
    user.save()


def set_up_course_registrations(row):
    print(row)

    user = User.objects.get(email=row[NEW_EMAIL])
    course_names = COURSES_BY_DEPARTMENT[row[DEPARTMENT]]
    set_course_reg(user, course_names)


def set_course_reg(user, course_names):
    curriculums = []
    for name in course_names:
        # print(name)
        curriculums.append(Curriculum.objects.get(name=name))

    course_ids = [curriculum.id for curriculum in curriculums]
    existing = CourseRegistration.objects.filter(user=user)
    for o in existing:
        if o.curriculum_id not in course_ids:
            o.delete()
    for i, curriculum_id in enumerate(course_ids):
        o, created = CourseRegistration.objects.get_or_create(
            user=user, curriculum_id=curriculum_id, defaults={"order": i}
        )
        if not created:
            o.order = i
            o.save()


def add_user_to_group(row):
    team, _ = Team.objects.get_or_create(name=row[TEAM_NAME].strip())
    user = User.objects.get(email=row[NEW_EMAIL])
    team.users.add(user)

    team = Team.objects.get(name="Problem Solving Foundation 1")
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

    def handle(self, *args, **options):
        path = options["path"]
        rocketchat_user = os.environ["ROCKETCHAT_USER"]
        rocketchat_pass = os.environ["ROCKETCHAT_PASS"]

        df = fetch_sheet(url=path)
        df = df[df[BROKEN] != 1]
        df = df[df[BROKEN] != "1"]
        # df = pd.read_csv(path)

        df.apply(update_user_email, axis=1)

        df.apply(add_user_to_group, axis=1)
        df.apply(set_up_course_registrations, axis=1)
        # client = Rocketchat()
        # client.login(rocketchat_user, rocketchat_pass)
        # try:
        #     df.apply(
        #         create_rocketchat_user_and_add_to_channel(
        #             client, ["ryan", "asanda", "sheena"]
        #         ),
        #         axis=1,
        #     )
        # except:
        #     import traceback

        #     print(traceback.format_exc())
        # finally:
        #     client.logout()