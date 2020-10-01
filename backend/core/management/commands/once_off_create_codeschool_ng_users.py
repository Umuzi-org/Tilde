from core.models import (
    User,
    UserProfile,
    Curriculum,
    Cohort,
    RecruitCohort,
    EmployerPartner,
)
from curriculum_tracking.models import CourseRegistration, AgileCard
from social_auth.models import SocialProfile
from django.core.management.base import BaseCommand

from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)
from google_helpers.utils import fetch_sheet


from django.utils.timezone import datetime
from datetime import timedelta

COHORT_INTAKE_NUMBER = 22

employer, _ = EmployerPartner.objects.get_or_create(name="Code Club NG")


def get_curriculum():
    return Curriculum.objects.get(short_name="web dev no nqf")


curriculum = get_curriculum()


def get_cohort():
    cohort, _ = Cohort.objects.get_or_create(
        cohort_number=22,
        label="CodeClubNG",
        defaults={
            "cohort_curriculum": curriculum,
            "start_date": datetime.today() + timedelta(days=1),
            "end_date": datetime.today() + timedelta(days=366),
        },
    )
    return cohort


cohort = get_cohort()
print(cohort)
# curriculum = get_curriculum()


def get_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/1pG4D_6UoQs95mNB2HR8bKnkoW7Aj-vPqRP8coKF2_Lo/edit#gid=1642960737"
    )
    df = df.dropna(subset=["Email"])
    return df


def process_row(row):
    email = row["Email"].strip().lower()
    github = row["Github Username"].strip()
    first_name = row["First Name"].strip()
    last_name = row["Surname"].strip()

    user, _ = User.objects.get_or_create(
        email=email, defaults={"first_name": first_name, "last_name": last_name,}
    )
    SocialProfile.objects.get_or_create(user=user, defaults={"github_name": github})

    RecruitCohort.objects.get_or_create(
        user=user,
        cohort=cohort,
        start_date=cohort.start_date,
        end_date=cohort.end_date,
        employer_partner=employer,
    )

    print(f"user: {user}")
    print()
    current_courses = CourseRegistration.objects.get_or_create(
        user=user, curriculum=curriculum
    )
    AgileCard.objects.filter(assignees__in=[user]).delete()
    generate_and_update_all_cards_for_user(user=user)


class Command(BaseCommand):
    def handle(self, *args, **options):

        df = get_df()
        df.apply(process_row, axis=1)

