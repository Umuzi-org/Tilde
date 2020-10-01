from django.core.management.base import BaseCommand, CommandError

from google_helpers.sheet_recruit_contacts import get_contacts_sheet_as_df
from google_helpers.sheet_github_names import get_sheet_as_df as get_github_sheet_as_df

import re

from core import models
from core import helpers
from social_auth import models as social_models
from django.contrib.auth import get_user_model
import datetime


User = get_user_model()


EXPECTED_CONTACT_COLUMNS = [
    "Cohort Number",
    "Curriculum",
    "Employer",
    "Last name",
    "First name",
    "Staff Member",
    "Gone",
    "Start date",
    "End date",
    "WhatsApp number",
    "Cell number",
    "Email Address",
    "Personal Email Address",
    "Product",
]


def _get_curriculum(long_ass_name):
    ui_design = (
        "ui",
        "ui design",
    )
    web = ("web dev", "web development")
    ds = ("data sci", "data science")
    copy = ("copy", "copywriting")

    CURRICULUMS = {
        "Strategy": ("strat", "strategy"),
        "Data Science": ds,
        "Web Dev": web,
        "Data Engineering": ("data eng", "data engineering"),
        "Copywriting": copy,
        "UI Design": ui_design,
        "Java": ("java", "java systems development"),
        "Multimedia": ("Multimedia", "Multimedia"),
        "UI Design with Advertising": ("ui and adv", "ui design and advertising"),
        "Advertising with Advertising": ("adv", "advertising"),
        "Copywriting with Advertising": ("copy and adv", "copywriting and advertising"),
        "Copywritting": copy,
        "Web Development": web,
        "Design": ui_design,
        "Coding - Data Science": ds,
        "Coding": web,
    }

    short_name, name = CURRICULUMS[long_ass_name]
    curriculum, _ = models.Curriculum.objects.get_or_create(
        short_name=short_name, name=name
    )
    return curriculum


def _save_contact(row):

    print(f"saving: {row['Email Address']}")
    DATE_FORMAT = "%d/%m/%Y"
    start_date = datetime.datetime.strptime(row["Start date"], DATE_FORMAT).date()
    end_date = datetime.datetime.strptime(row["End date"], DATE_FORMAT).date()

    user, _ = User.objects.get_or_create(
        email=row["Email Address"],
        defaults={
            "active": row["Gone"] != "yes",
            "first_name": row["First name"],
            "last_name": row["Last name"],
            "is_recruit": True,
            "is_staff": row["Staff Member"] == "yes",
            "is_superuser": False,
        },
    )

    employer_partner, _ = models.EmployerPartner.objects.get_or_create(
        name=row["Employer"]
    )

    curriculum = _get_curriculum(row["Curriculum"])
    user_profile, _ = models.UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "cellphone_number": row["Cell number"],
            "whatsapp_number": row["WhatsApp number"],
            "personal_email": row["Personal Email Address"],
        },
    )

    cohort, _ = models.Cohort.objects.get_or_create(
        cohort_number=int(row["Cohort Number"]),
        cohort_curriculum=curriculum,
        defaults={"start_date": start_date, "end_date": end_date},
    )
    cohort.start_date = min([cohort.start_date, start_date])
    cohort.end_date = max([cohort.end_date, end_date])

    recruit_cohort = models.RecruitCohort.objects.get_or_create(
        user=user,
        defaults={
            "employer_partner": employer_partner,
            "cohort": cohort,
            "start_date": start_date,
            "end_date": end_date,
        },
    )

    products = [s.strip() for s in row["Product"].split(",")]
    for product_name in products:
        if not product_name:
            continue
        team, _ = models.ProductTeam.objects.get_or_create(name=product_name)
        models.ProductTeamMembership.objects.get_or_create(product_team=team, user=user)


def sync_all_payroll_users():
    df = get_contacts_sheet_as_df()
    for column in EXPECTED_CONTACT_COLUMNS:
        assert column in df.columns, f"Column {column} not found!"
    df.apply(_save_contact, axis=1)


def update_user_github_name(row):
    email = row["Email Address"]
    github_name = row["username"].strip()

    print(f"{email} => {github_name}")
    first_name, last_name = helpers.get_first_and_last_names_from_business_email(email)
    user, _ = User.objects.get_or_create(
        email=email, defaults={"first_name": first_name, "last_name": last_name,}
    )
    profile, _ = social_models.SocialProfile.objects.get_or_create(user=user)

    profile.github_name = github_name
    profile.save()


def get_user_github_names():
    df = get_github_sheet_as_df()
    df.apply(update_user_github_name, axis=1)


def make_sure_all_existing_users_have_profiles():
    for user in User.objects.all():
        models.UserProfile.objects.get_or_create(user=user)


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_all_payroll_users()
        get_user_github_names()
        make_sure_all_existing_users_have_profiles()
        # get_user_rocketchat_names()
