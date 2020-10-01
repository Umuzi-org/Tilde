"""figuring out who plagerised is a bit hard. This uses git commit history to try figure it our"""

from django.core.management.base import BaseCommand
from core.models import User, Cohort, RecruitCohort
from curriculum_tracking.models import RecruitProject
from git_real.models import Commit
from git_real.management.commands.git_real_pull_commits import (
    scrape_and_save_repo_commits,
)
import csv


def get_matching_projects(users):
    projects = []
    for user in users:
        if "sheena" in user.email:
            continue
        projects.extend(RecruitProject.objects.filter(recruit_users__in=[user]))
    return projects


def generate_plagerism_hint_report(users):

    projects = get_matching_projects(users)
    for project in projects:
        print(project)
        print(f"project id = {project.id}")
        print(f"repository = {project.repository}")
        print(f"repository.id = {project.repository.id}")

        Commit.objects.filter(repository=project.repository).delete()
        scrape_and_save_repo_commits(project.repository)
        emails = [o.email for o in project.recruit_users.all()]

        assignee_github_names = [
            o.social_profile.github_name for o in project.recruit_users.all()
        ]

        commits = Commit.objects.filter(repository=project.repository)
        commit_count = commits.count()
        # if commit_count:
        #     breakpoint()
        first_commit = commits.order_by("datetime").first()
        last_commit = commits.order_by("datetime").last()

        commit_authors = commits.values("author_github_name").distinct()

        ret = {
            "content_item": project.content_item.title,
            "repo": project.repository.full_name,
            "assignee_users": emails,
            "assignee_gitnub_names": assignee_github_names,
            "commit_count": commit_count,
            "first_commit": first_commit.datetime.strftime("%c")
            if commit_count
            else None,
            "last_commit": last_commit.datetime.strftime("%c")
            if commit_count
            else None,
            "commit_authors": [
                s
                for s in [o["author_github_name"] for o in commit_authors.all()]
                if "umuzibot" != s
            ],
        }
        yield (ret)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("cohort", type=str)
        # parser.add_argument("content_item", type=str)

    def handle(self, *args, **options):
        cohort_name = options["cohort"]
        # content_item_name = options["content_item"]
        cohort = Cohort.get_from_short_name(cohort_name)

        users = [o.user for o in RecruitCohort.objects.filter(cohort=cohort)]

        report_data = list(generate_plagerism_hint_report(users))
        report_data.sort(key=lambda d: d["content_item"])

        headings = [
            "content_item",
            "repo",
            "assignee_users",
            "assignee_gitnub_names",
            "commit_count",
            "first_commit",
            "last_commit",
            "commit_authors",
        ]
        with open(f"gitignore/project_plagerism_hints_{cohort}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for row in report_data:
                if not row["commit_authors"]:
                    continue
                writer.writerow([row[s] for s in headings])


"""
python manage.py plagiarism_hint_export "C22 web dev"
python manage.py plagiarism_hint_export "C22 data science"
"""
