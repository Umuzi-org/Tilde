from curriculum_tracking.models import AgileCard
from google_helpers.utils import fetch_sheet
from django.core.management.base import BaseCommand

from git_real import helpers as git_helpers
from git_real.constants import GIT_REAL_BOT_USERNAME
import re

CARD_ID = "Card Id (integer)"
REPO = "Repo url incorrect. It should be ... (fill in the full repo url: https://github.com/[stuff].git)"
APPROVED = "Approved"


def get_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/1Vt_EbalUILVgyDG2qU8zY1KkszNc7KuqQK-s5XpnP3c/edit#gid=1544474779"
    )
    df = df.dropna(subset=[CARD_ID])
    df = df.dropna(subset=[REPO])
    df = df[df[APPROVED] == "yes"]
    return df


def process_row(row):
    repo_url = row[REPO]
    found = re.search("https://github.com/(.*)\.git", repo_url)
    if not found:
        print(f"bad url: {repo_url}")
        return
    repo_full_name = found.groups()[0]
    try:
        repo_dict = git_helpers.get_repo(
            github_auth_login=GIT_REAL_BOT_USERNAME, repo_full_name=repo_full_name
        )
    except AssertionError:
        print(f"bad url: {repo_url}")
        return

    repo = git_helpers.save_repo(
        repo_dict
    )  # note thet the repo itself doesn't "belong" to anyone

    try:
        card = AgileCard.objects.get(pk=int(row[CARD_ID]))
    except AgileCard.DoesNotExist:
        print(f"bad card if: {row[CARD_ID]}")
        return

    card.recruit_project.repo = repo
    card.recruit_project.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = get_df()
        df.apply(process_row, axis=1)