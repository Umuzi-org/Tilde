import os
import re
import datetime
from django.db.models import Q

from django.core.management.base import BaseCommand, CommandError
from core import models as core_models
from git_real import models
from git_real.constants import CLONE_DESTINATION
from django.utils import timezone


cutoff_date = timezone.now() - datetime.timedelta(days=90)
cutoff_date = cutoff_date.astimezone()


def _repo_clone_path(repo):
    return CLONE_DESTINATION / repo.full_name


def _clone_repo_if_not_exists(repo):
    repo_path = _repo_clone_path(repo)
    if os.path.exists(repo_path):
        return
    command = f"git clone {repo.ssh_url} {repo_path}"
    print(command)
    os.system(command)


def _get_branch_names(repo):
    cwd = os.getcwd()
    os.chdir(_repo_clone_path(repo))
    branches = os.popen("git branch -a").read().split("\n")
    os.chdir(cwd)
    branch_names = [
        found.groups()[0]
        for found in [re.search("origin\/(.*)$", s) for s in branches if "->" not in s]
        if found
    ]
    return [s for s in branch_names if s != "master"] + [
        "master"
    ]  # sort stuff so master is at the end


def _get_branch_commits(repo, branch_name):
    cwd = os.getcwd()
    os.chdir(_repo_clone_path(repo))
    print(f"EXECUTING: git checkout {branch_name}")
    os.system(f"git checkout {branch_name}")
    print(f"EXECUTING: git pull")
    os.system(f"git pull -f")
    git_log = os.popen("git log").read()
    os.chdir(cwd)

    for commit in re.findall(
        "commit (.*)\nAuthor: (.*) <(.*)>\nDate:(.*)\n\n(.*)\n", git_log
    ):
        commit = dict(
            zip(
                (
                    "commit_hash",
                    "author_github_name",
                    "author_email",
                    "datetime",
                    "message",
                ),
                (s.strip() for s in commit),
            )
        )
        commit["branch"] = branch_name
        # dt = commit["datetime"].split("+")[0].split("-")[0].strip()
        # print(dt)
        commit["datetime"] = timezone.datetime.strptime(
            commit["datetime"], "%a %b %d %H:%M:%S %Y %z"
        )  # xxx
        # TODO TIMEZONE info (#158)
        # "Tue Oct 18 12:25:50 2016 +0200",

        if commit["datetime"] < cutoff_date:
            break

        user_profile = core_models.UserProfile.objects.filter(
            Q(user__social_profile__github_name=commit["author_github_name"])
            | Q(personal_email=commit["author_email"])
        ).first()

        if user_profile:
            commit["user"] = user_profile.user
        else:
            commit["user"] = core_models.User.objects.filter(
                email=commit["author_email"]
            ).first()

        yield commit


def scrape_and_save_repo_commits(repo):
    os.makedirs(CLONE_DESTINATION, exist_ok=True)
    _clone_repo_if_not_exists(repo)
    for branch_name in _get_branch_names(repo):
        print(f"Branch: {branch_name}")

        for commit in _get_branch_commits(repo, branch_name):
            obj, created = models.Commit.objects.get_or_create(
                repository=repo, commit_hash=commit["commit_hash"], defaults=commit
            )
            if created:
                break


def update_all_commit_logs():
    all_repos = models.Repository.objects.all()
    count = len(all_repos)
    for i, repo in enumerate(all_repos):
        print(f"Repo {i+1} of {count}: {repo}")
        scrape_and_save_repo_commits(repo)


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_all_commit_logs()
