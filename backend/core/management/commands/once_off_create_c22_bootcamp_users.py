from core.models import (
    User,
    UserProfile,
    Curriculum,
    Cohort,
    RecruitCohort,
    EmployerPartner,
)
from curriculum_tracking.models import CourseRegistration
from social_auth.models import SocialProfile
from django.core.management.base import BaseCommand

from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)
from google_helpers.utils import fetch_sheet

COHORT_INTAKE_NUMBER = 22

COHORT_ID_DATA_SCI = 50
COHORT_ID_WEB_DEV = 51


def get_cohort(pk, name_contains):
    cohort = Cohort.objects.get(pk=pk)
    for s in name_contains:
        assert s in str(cohort), f"{s} not in {cohort}"
    return cohort


cohort_web_dev = get_cohort(COHORT_ID_WEB_DEV, ["22", "web", "boot"])
cohort_data_sci = get_cohort(COHORT_ID_DATA_SCI, ["22", "data", "boot"])
employer, _ = EmployerPartner.objects.get_or_create(name="Umuzi")
employer.save()


def get_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/1UWQRfdw95gnKyqoHNwn2yX8iJPdlued46goxZtVlPGQ/edit#gid=786487706"
    )
    df = df.dropna(subset=["Gmail Address"])
    return df


def process_row(row):
    email = row["Gmail Address"].strip().lower()
    github = row["Github Name"]
    dept_name = row["Department"]
    first_name = row["First name"]
    last_name = row["Last name"]

    user, _ = User.objects.get_or_create(
        email=email, defaults={"first_name": first_name, "last_name": last_name,}
    )
    SocialProfile.objects.get_or_create(user=user, defaults={"github_name": github})

    if dept_name == DEPT_DS:
        cohort = cohort_data_sci
        curriculums = data_science_curriculums

    elif dept_name == DEPT_WEB:
        cohort = cohort_web_dev
        curriculums = web_dev_curriculums

    else:
        raise Exception(f"unrecognised department '{dept_name}'")

    RecruitCohort.objects.get_or_create(
        user=user,
        cohort=cohort,
        start_date=cohort.start_date,
        end_date=cohort.end_date,
        employer_partner=employer,
    )

    current_courses = CourseRegistration.objects.filter(user=user).order_by("order")
    if current_courses:
        assert [
            o.curriculum for o in current_courses
        ] == curriculums, f"Course mismatch:\n\t{[o.curriculum for o in current_courses]} != {curriculums}"
    else:
        for i, o in enumerate(curriculums):
            CourseRegistration.objects.create(order=i, curriculum=o, user=user)
    current_courses = CourseRegistration.objects.filter(user=user).order_by("order")

    print(f"user: {user}")
    print(f"department: {dept_name}")
    print(f"cohort: {cohort}")
    print(f"courses: {[o.curriculum for o in current_courses]}")
    print()
    generate_and_update_all_cards_for_user(user=user)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # for row in [
        #     {
        #         "Gmail Address": "sheena.oconnell@gmail.com",
        #         "Github Name": "sheenarbw2",
        #         "Department": DEPT_WEB,
        #         "First name": "Sheena",
        #         "Last name": "O'Connell",
        #     },
        #     {
        #         "Gmail Address": "sheena@prelude.tech",
        #         "Github Name": "sheenarbw3",
        #         "Department": DEPT_DS,
        #         "First name": "Sheena",
        #         "Last name": "O'Connell",
        #     },
        # ]:
        #     process_row(row)
        df = get_df()
        df.apply(process_row, axis=1)

