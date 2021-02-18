from django.core.management.base import BaseCommand


from google_helpers.utils import fetch_sheet

INTAKE_NUMBER = 23

from core.models import User, Team
from social_auth.models import SocialProfile
from curriculum_tracking.models import CourseRegistration
import datetime

now = timezone.now()
team = Team.objects.get_or_create(name="ds bootcamp sept 20")[0]


def get_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/15SduszqpCEenMKPXw_yz5GjEtJbDqKfDtFWmmRKNFr0/edit?ts=5f647abb#gid=0"
    )
    df = df.dropna(subset=["Email"])
    return df


def process_row(row):
    # print(row)
    email = row["Email"].strip()
    name = row["First Name"].strip()
    last_name = row["Last Name"].strip()
    github = row["github username"].strip()

    if not last_name and len(name.split()) > 1:
        last_name = name.split()[-1]
    if len(name.split()) > 1:
        first_name = name.split()[0]
    else:
        first_name = name

    user = User.objects.get_or_create(
        email=email, defaults={"first_name": first_name, "last_name": last_name}
    )[0]

    if github:
        profile = SocialProfile.objects.get_or_create(user=user)[0]
        profile.github_name = github
        profile.save()

    try:
        profile = SocialProfile.objects.get(user=user)
        user.active = bool(profile.github_name)
    except SocialProfile.DoesNotExist:
        user.active = False
    user.save()

    team.user_set.add(user)

    CourseRegistration.objects.get_or_create(
        user=user, curriculum_id=33, order=1
    )  # intro to tilde
    CourseRegistration.objects.get_or_create(
        user=user, curriculum_id=20, order=2
    )  # ds pre boot
    CourseRegistration.objects.get_or_create(
        user=user, curriculum_id=28, order=3
    )  # ds boot

    print(f"{user} active = {user.active}")
    # AgileCard.objects.filter(assignees__in=[user]).delete()
    # generate_and_update_all_cards_for_user(user, None)


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = get_df()
        df.apply(process_row, axis=1)