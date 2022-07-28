dontuse
from django.core.management.base import BaseCommand
from core.models import TeamMembership
from curriculum_tracking.models import ContentItem, RecruitProject, AgileCard
import datetime
import os
from pathlib import Path
from ..helpers import get_group
import shutil
import re
import csv

DATE_FORMAT = "%-d-%b-%y"


def get_project(user, content_title):
    return RecruitProject.objects.filter(
        content_item__title=content_title, recruit_users__in=[user]
    ).first()


def download_repos(user, path, content_title):
    project = get_project(user, content_title)
    if project == None or project.repository == None:
        return

    ssh_url = project.repository.ssh_url
    clone_path = path / f"{user.email} - {content_title}"
    if clone_path.exists():
        return
        shutil.rmtree(clone_path)

    command = f'git clone {ssh_url} "{clone_path}"'
    print(command)
    os.system(command)


def get_github_page_url(user, content_title):
    project = get_project(user, content_title)
    if project == None:
        return

    repo_url = project.repository and project.repository.ssh_url
    url = project.link_submission or repo_url

    if not url:
        return

    found = (
        re.search("git@github.com:(.*)/(.*).git", url)
        or re.search("https://github.com/(.*)/(.*)$", url)
        or re.search("https://github.com/(.*)/(.*).git", url)
    )
    if found:
        git_user, git_repo = found.groups()
        return f"https://{git_user}.github.io/{git_repo}"

    found = re.search("https://(.*).github.io/(.*)", url)
    if found:
        return url.strip().strip("/")
    pass


def get_card_data(user):
    data = {"all_project_titles": []}
    cards = AgileCard.objects.filter(
        assignees__in=[user], content_item__content_type=ContentItem.PROJECT
    ).order_by("order")

    for card in cards:
        tag_names = [
            o.name
            for o in list(card.flavours.all()) + list(card.content_item.tags.all())
        ]

        data[f"{card.content_item.title}: order"] = card.order
        data[f"{card.content_item.title}: status"] = card.status
        data[f"{card.content_item.title}: tags"] = tag_names
        data[f"{card.content_item.title}: weight"] = card.content_item.story_points
        data[f"{card.content_item.title}: instructions"] = card.content_item.url
        data[f"{card.content_item.title}: start_time"] = (
            card.due_time.strftime(DATE_FORMAT) if card.due_time else None
        )
        data[f"{card.content_item.title}: start_time"] = (
            card.start_time.strftime(DATE_FORMAT) if card.start_time else None
        )
        data[f"{card.content_item.title}: review_request_time"] = (
            card.review_request_time.strftime(DATE_FORMAT)
            if card.review_request_time
            else None
        )
        data[f"{card.content_item.title}: complete_time"] = (
            card.complete_time.strftime(DATE_FORMAT) if card.complete_time else None
        )
        data["all_project_titles"].append(card.content_item.title)
    return data


def get_tag_summaries(card_data):
    tag_data = {}
    for title in card_data["all_project_titles"]:
        weight = card_data[f"{title}: weight"]
        status = card_data[f"{title}: status"]
        for tag in card_data[f"{title}: tags"]:
            tag_data[f"{tag}_total_weight"] = tag_data.get(f"{tag}_total_weight", 0)
            tag_data[f"{tag}_complete_weight"] = tag_data.get(
                f"{tag}_complete_weight", 0
            )
            tag_data[f"{tag}_incomplete_weight"] = tag_data.get(
                f"{tag}_incomplete_weight", 0
            )

            tag_data[f"{tag}_total_weight"] += weight
            if status == AgileCard.COMPLETE:
                tag_data[f"{tag}_complete_weight"] += weight
            else:
                tag_data[f"{tag}_incomplete_weight"] += weight
    return tag_data


def get_report_data(user, path):
    download_repos(user=user, path=path, content_title="Bootcamp Writing Assignment")
    portfolio = get_github_page_url(
        user=user, content_title="Build your first personal website"
    )
    card_data = get_card_data(user=user)
    data = {
        "email": user.email,
        "github_profile": f"https://github.com/{user.social_profile.github_name}",
        "portfolio": portfolio,
    }

    tag_data = get_tag_summaries(card_data)

    for key, value in card_data.items():
        data[f"project: {key}"] = value

    for key, value in tag_data.items():
        data[f"tag: {key}"] = value

    return data


def get_headings_from_dicts(rows):
    headings = []
    for row in rows:
        for key in row:
            if key not in headings:
                headings.append(key)
    return headings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("group_name", type=str)

    def handle(self, *args, **options):
        group_name = options["group_name"]
        path = Path(
            f"gitignore/high_res_report_{group_name}_{datetime.date.today().strftime(DATE_FORMAT)}",
        )
        os.makedirs(path, exist_ok=True)

        group = get_group(group_name)

        users = [o.user for o in TeamMembership.objects.filter(group=group)]

        rows = [get_report_data(user=user, path=path) for user in users]

        headings = get_headings_from_dicts(rows)

        with open(path / "data.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)
            for row in rows:
                writer.writerow([row.get(heading) for heading in headings])
