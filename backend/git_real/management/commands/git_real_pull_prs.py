from django.core.management.base import BaseCommand, CommandError


from social_auth.github_api import Api
from git_real.constants import PERSONAL_GITHUB_NAME
from git_real import models
from git_real.helpers import strp_github_standard_time


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

        github_user = review["user"]["login"]
        defaults = {
            "body": review["body"],
            "submitted_at": review.get("submitted_at")
            and strp_github_standard_time(
                timestamp=review["submitted_at"],
            ),
            "commit_id": review["commit_id"],
            "state": review["state"],
            "user": get_user_from_github_name(github_user),
        }
        review_obj, created = models.PullRequestReview.objects.get_or_create(
            pull_request=pr,
            number=review["id"],
            author_github_name=github_user,
            # submitted_at=submitted_at,
            defaults=defaults,
        )
        if not created:
            review_obj.update(**defaults)
            review_obj.save()


def scrape_repo_prs(api, repo):
    pull_requests = api.request_pages(
        f"repos/{repo.full_name}/pulls", params={"state": "all"}, response404=404
    )
    for pr in pull_requests:
        if pr == 404:
            continue
        github_user = pr["user"]["login"]
        defaults = {
            "state": pr["state"],
            "title": pr["title"],
            "body": pr["body"],
            "created_at": strp_github_standard_time(
                pr["created_at"],
            ),
            "updated_at": pr["updated_at"]
            and strp_github_standard_time(
                pr["updated_at"],
            ),
            "closed_at": pr["closed_at"]
            and strp_github_standard_time(
                pr["closed_at"],
            ),
            "merged_at": pr["merged_at"]
            and strp_github_standard_time(
                pr["merged_at"],
            ),
            "author_github_name": github_user,
            "assignees": [d["login"] for d in pr["assignees"]],
            "user": get_user_from_github_name(github_user),
        }
        update_pr = {
            k: defaults[k]
            for k in [
                "state",
                "title",
                "body",
                "updated_at",
                "closed_at",
                "merged_at",
                "assignees",
                "user",
            ]
        }

        pr_object, pr_created = models.PullRequest.objects.get_or_create(
            number=pr["number"],
            repository=repo,
            defaults=defaults,
        )
        if not pr_created:
            pr_object.update(**update_pr)

        # scrape_pr_comments(api, pr_object)
        # TODO: write ETL for pull request comments (#159)

        scrape_pull_request_reviews(api, pr_object)


def scrape_pull_requests_from_github():
    api = Api(PERSONAL_GITHUB_NAME)
    for repo in models.Repository.objects.filter(archived=False):
        scrape_repo_prs(api, repo)


class Command(BaseCommand):
    def handle(self, *args, **options):
        scrape_pull_requests_from_github()
