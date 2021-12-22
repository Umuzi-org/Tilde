from django.core.management.base import BaseCommand
from social_auth.github_api import Api
from git_real.constants import PERSONAL_GITHUB_NAME
from git_real import models
from django.db.models import Q
from curriculum_tracking.models import AgileCard
from core.models import User


def get_user_from_github_name(github_name):
    try:
        return User.objects.get(social_profile__github_name=github_name)
    except User.DoesNotExist:
        return None


def scrape_pull_request_reviews(api, pr):
    reviews = api.request_pages(
        f"repos/{pr.repository.full_name}/pulls/{pr.number}/reviews"
    )
    for review in reviews:
        models.PullRequestReview.create_or_update_from_github_api_data(
            pull_request=pr, review_data=review
        )


def scrape_repo_prs(api, repo):
    pull_requests = api.request_pages(
        f"repos/{repo.full_name}/pulls", params={"state": "all"}, response404=404
    )
    for pr in pull_requests:
        if pr == 404:
            continue
        pr_object = models.PullRequest.create_or_update_from_github_api_data(
            pull_request_data=pr, repo=repo
        )
        scrape_pull_request_reviews(api, pr_object)


def scrape_pull_requests_from_github():
    api = Api(PERSONAL_GITHUB_NAME)
    for repo in (
        models.Repository.objects.filter(
            recruit_projects__recruit_users__active__in=[True],
        )
        .filter(
            Q(recruit_projects__agile_card__status=AgileCard.IN_PROGRESS)
            | Q(recruit_projects__agile_card__status=AgileCard.IN_REVIEW)
            | Q(recruit_projects__agile_card__status=AgileCard.REVIEW_FEEDBACK)
        )
        .order_by("-recruit_projects__start_time")
    ):
        scrape_repo_prs(api, repo)


class Command(BaseCommand):
    def handle(self, *args, **options):
        scrape_pull_requests_from_github()
