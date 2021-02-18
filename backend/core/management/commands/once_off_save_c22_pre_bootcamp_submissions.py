from core.models import User
from curriculum_tracking.models import ContentItem, AgileCard, RecruitProject
from git_real.models import Repository
from django.utils import timezone
from django.core.management.base import BaseCommand
from google_helpers.utils import fetch_sheet
import re

GIT_EXCERCISES_ID = 288
PRE_BOOTCAMP_CHALLENGES_ID = 416

content_items = {
    "git-exercises": ContentItem.objects.get(pk=288),
    "pre-bootcamp-challenges": ContentItem.objects.get(pk=416),
}


def clean_github_username(row):
    s = row["Please enter your github name"]
    return s.split("/")[-1].strip()


def clean_project_url(row):
    s = row["Project instructions url "]
    if "pre-bootcamp-challenges" in s:
        return "pre-bootcamp-challenges"
    if "git-exercises" in s:
        return "git-exercises"


def clean_repo_url(row):
    s = row["Link to git repo"].strip()
    if s == "":
        return
    if s is None:
        return
    print(s)
    if "Umuzi-org/tech-department" in s:
        return None
    if "?" in s:
        return None
    if s.startswith("https://github.com"):
        found = re.search("https://github.com/(.*)/(.*)/", f"{s}/")
        if not found:
            return None
        user, repo = found.groups()

        ret = f"{user}/{repo}"

    if "github.io" in s:

        clean_user = clean_github_username(row)
        user, repo = re.search("https://(.*).github.io/(.*)", s).groups()
        # return f"https://github.com/{user}/{repo}"
        assert clean_user.lower() == user.lower(), f"{user} != {clean_user}"
        ret = f"{clean_user}/{repo}"

    if ret.endswith(".git"):
        ret = ret[:-4]
    ret = ret.strip("/").strip(".")
    # print(ret)
    return ret


def save_project_and_update_card(row):
    try:
        user = User.objects.get(social_profile__github_name=row["clean_github_name"])
    except User.DoesNotExist:
        print(f"cant find user with github name: {row['clean_github_name']}")
        return
    content_item = content_items[row["clean_project_url"]]

    try:
        card = AgileCard.objects.get(content_item=content_item, assignees__in=[user])
    except AgileCard.DoesNotExist:
        print(f"cant find card: {user} {content_item}")
        return

    repo_full_name = row["repo_full_name"]

    repo, _ = Repository.objects.get_or_create(
        full_name=row["repo_full_name"],
        user=user,
        defaults={
            "owner": repo_full_name.split("/")[0],
            "ssh_url": f"git@github.com:{repo_full_name}.git",
            "created_at": timezone.now(),
            "private": False,
            "archived": False,
        },
    )

    project = RecruitProject.objects.filter(
        content_item=content_item,
        recruit_users__in=[user],
    ).first()
    if project:
        project.repository = repo
        project.save()

        if card.status in [AgileCard.READY, AgileCard.BLOCKED]:
            breakpoint()
            pass
    else:
        project = RecruitProject.objects.create(
            content_item=content_item,
            repository=repo,
        )
        project.recruit_users.add(user)
        for flavour in card.flavours.all():
            project.flavours.add(flavour)

    card.recruit_project = project
    card.save()

    if card.status in [AgileCard.BLOCKED, AgileCard.READY]:
        project = card.recruit_project
        project.request_review()
        card.status = AgileCard.IN_REVIEW
        card.save()
        project.save()
    # if card.status == AgileCard.BLOCKED:

    # recruit_user=self.assignees.first(),
    # flavour_names=self.flavour_names,

    # card.save()
    # print(user)
    # print(card)
    # print(project)
    # pass

    # card.recruit_project.repository


def get_df():
    df = fetch_sheet(
        url="https://docs.google.com/spreadsheets/d/1I_sQ8N08pi-oNqVIAk5Q7pb5G_kDMEzTbA0-_aJnAGo/edit#gid=999865580"
    )
    df = df.dropna(subset=["Timestamp"])
    df["clean_github_name"] = df.apply(clean_github_username, axis=1)
    df["clean_project_url"] = df.apply(clean_project_url, axis=1)
    df["repo_full_name"] = df.apply(clean_repo_url, axis=1)

    # breakpoint()
    df = df.dropna(
        subset=["repo_full_name"],
    )
    df = df.dropna(
        subset=["clean_project_url"],
    )
    df = df.drop_duplicates(
        subset=["clean_project_url", "clean_github_name"], keep="last"
    )

    return df


class Command(BaseCommand):
    def handle(self, *args, **options):
        df = get_df()
        df.apply(save_project_and_update_card, axis=1)
