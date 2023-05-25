from django.core.management.base import BaseCommand
from google_helpers.utils import fetch_sheet
from curriculum_tracking.models import AgileCard
from core.models import User
from git_real.helpers import fetch_and_save_repo
from git_real.constants import GIT_REAL_BOT_USERNAME


REPO_COL = "Repo url incorrect. It should be ... (fill in the full repo url: https://github.com/[stuff].git)"


def get_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/1Vt_EbalUILVgyDG2qU8zY1KkszNc7KuqQK-s5XpnP3c"
    )
    df = df.dropna(subset=["Approved"])
    df = df[df["Approved"] == "yes"]
    df = df[df[REPO_COL].str.endswith(".git")]
    df = df[df[REPO_COL].str.startswith("https://github.com/")]

    return df


def get_repo_full_name(repo_url):
    return repo_url[19:-4]


def process_row(row):
    print(row)
    card_id = row["Card Id (integer)"]
    email = row["Email Address"]
    user = User.objects.get(email=email)
    try:
        card = AgileCard.objects.get(pk=int(card_id))
    except AgileCard.DoesNotExist:
        print("Does not exist")
        return
    if user not in card.assignees.all():
        print("Error: user not assigned to card")

    repo = fetch_and_save_repo(
        github_auth_login=GIT_REAL_BOT_USERNAME,
        repo_full_name=get_repo_full_name(row[REPO_COL]),
    )
    project = card.recruit_project
    project.repository = repo
    project.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = get_df()
        df.apply(process_row, axis=1)
