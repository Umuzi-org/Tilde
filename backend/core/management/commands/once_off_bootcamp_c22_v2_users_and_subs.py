from core.models import (
    User,
    UserProfile,
    Curriculum,
    Cohort,
    RecruitCohort,
    EmployerPartner,
)
from curriculum_tracking.models import ContentItem, AgileCard, RecruitProject
from git_real.models import Repository
from django.utils import timezone
from curriculum_tracking.models import CourseRegistration
from social_auth.models import SocialProfile
from django.core.management.base import BaseCommand

from curriculum_tracking.card_generation_helpers import (
    generate_and_update_all_cards_for_user,
)
from google_helpers.utils import fetch_sheet
from ..bootcamp_load_helpers import *
from curriculum_tracking.models import ContentItem, AgileCard, RecruitProject

COHORT_ID_DATA_SCI = 50
COHORT_ID_WEB_DEV = 51


def get_cohort(pk, name_contains):
    cohort = Cohort.objects.get(pk=pk)
    for s in name_contains:
        assert s in str(cohort), f"{s} not in {cohort}"
    return cohort


cohort_web_dev = get_cohort(COHORT_ID_WEB_DEV, ["22", "web", "boot"])
employer, _ = EmployerPartner.objects.get_or_create(name="Umuzi")
employer.save()


def get_users_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/16ohoj81oF4Gws979tY02FYaKsxBATz7kN8yHudc-OeM"
    )
    df = df.dropna(subset=["Email Address"])
    return df


def process_users_row(row):
    email = row["Email Address"].strip().lower()
    github = row["Github"]
    first_name = row["First name"]
    last_name = row["Last name"]

    user, _ = User.objects.get_or_create(
        email=email, defaults={"first_name": first_name, "last_name": last_name,}
    )

    github = github.split("/")[-1]

    SocialProfile.objects.get_or_create(user=user, defaults={"github_name": github})

    cohort = cohort_web_dev
    curriculums = web_dev_curriculums

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
    print(f"cohort: {cohort}")
    print(f"courses: {[o.curriculum for o in current_courses]}")
    print()
    generate_and_update_all_cards_for_user(user=user)


content_items = {
    "git-exercises": ContentItem.objects.get(pk=288),
    "pre-bootcamp-challenges": ContentItem.objects.get(pk=416),
}


def get_subs_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/16kabZgFpZaBBUfuzvd5cWqKJbNWzMPZdL3Caq0q7veg/edit#gid=650997048"
    )
    df = df.dropna(subset=["Email Address"])
    return df


def process_subs_row(row):
    user = User.objects.get(email=row["Email Address"])
    content_item = content_items[row["What project are you handing in?"]]
    card = AgileCard.objects.get(content_item=content_item, assignees__in=[user])

    repo_full_name = row["Link to your git repo"][19:]

    repo, _ = Repository.objects.get_or_create(
        full_name=repo_full_name,
        user=user,
        defaults={
            "owner": repo_full_name.split("/")[0],
            "ssh_url": f"git@github.com:{repo_full_name}.git",
            "created_at": timezone.datetime.now(),
            "private": False,
            "archived": False,
        },
    )

    project = RecruitProject.objects.filter(
        content_item=content_item, recruit_users__in=[user],
    ).first()
    if project:
        project.repository = repo
        project.save()

        if card.status in [AgileCard.READY, AgileCard.BLOCKED]:
            breakpoint()
            pass
    else:
        project = RecruitProject.objects.create(
            content_item=content_item, repository=repo,
        )
        project.recruit_users.add(user)
        for flavour in card.content_flavours.all():
            project.flavours.add(flavour)

    card.recruit_project = project
    card.save()

    if card.status in [AgileCard.BLOCKED, AgileCard.READY]:
        project = card.recruit_project
        project.request_review()
        card.status = AgileCard.IN_REVIEW
        card.save()
        project.save()


class Command(BaseCommand):
    def handle(self, *args, **options):

        # df = get_users_df()
        # df.apply(process_users_row, axis=1)

        df = get_subs_df()
        df.apply(process_subs_row, axis=1)

