from django.core.management.base import BaseCommand


from google_helpers.utils import fetch_sheet

COHORT_INTAKE_NUMBER = 23

from core.models import User, UserGroup, UserGroupMembership
from social_auth.models import SocialProfile
from curriculum_tracking.models import CourseRegistration, AgileCard
import datetime


from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)


FIRST_NAME = "Name"
LAST_NAME = "Surname"
EMAIL = "Email Address"
GIT = "GitHub Username"
COURSE = "Course"


GROUP_NAME = "Boot 12 Oct 2020"
TODO = "todo"
group = UserGroup.objects.get_or_create(name=GROUP_NAME)[0]

DS = "ds"
DE = "de"

TILDE_INTRO = 33
DS_PRE_BOOT = 20
DS_BOOT = 28
DE_PRE_BOOT = 36
DE_BOOT = 35


def get_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/1xOwSUOc7iiyi08QvIBbSna0HRMaX6GyLi8jdCn5Q2rU/edit#gid=101393965"
    )
    df = df.dropna(subset=[EMAIL])
    df = df.dropna(subset=[TODO])
    df = df[df[TODO] == 1]
    df.columns = [s.strip() for s in df.columns]
    return df


def set_course_reg(user, course_ids):
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


def process_row(row):
    # print(row)
    email = row[EMAIL].strip()
    first_name = row[FIRST_NAME].strip()
    last_name = row[LAST_NAME].strip()
    github = row[GIT].strip()
    course = row[COURSE].strip()

    user = User.objects.get_or_create(
        email=email, defaults={"first_name": first_name, "last_name": last_name}
    )[0]
    user.active = True
    user.save()

    profile = SocialProfile.objects.get_or_create(user=user)[0]
    profile.github_name = github
    profile.save()

    UserGroupMembership.objects.get_or_create(
        user=user, group=group, permission_student=True
    )

    if course == DS:
        courses = [TILDE_INTRO, DS_PRE_BOOT, DS_BOOT]
        set_course_reg(user, courses)
    elif course == DE:
        courses = [TILDE_INTRO, DE_PRE_BOOT, DE_BOOT]
        set_course_reg(user, courses)
    else:
        waaaat
    print(f"{course} {email}")


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = get_df()
        df.apply(process_row, axis=1)
