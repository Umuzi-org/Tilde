from django.db import models
from django.contrib.postgres.fields import ArrayField

from model_mixins import Mixins

from core.models import User


class Repository(models.Model, Mixins):
    owner = models.CharField(max_length=50)
    full_name = models.CharField(max_length=150, unique=True)
    ssh_url = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField()
    private = models.BooleanField()
    archived = models.BooleanField()

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.ssh_url


class Commit(models.Model, Mixins):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    commit_hash = models.CharField(max_length=40)
    author_github_name = models.CharField(max_length=100)
    author_email = models.CharField(max_length=240)
    message = models.TextField()
    branch = models.CharField(max_length=150)
    datetime = models.DateTimeField()

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # TODO Denormalise (#157)

    def __str__(self):
        ellipse = ""
        cutoff = 40
        if len(self.message) > cutoff:
            ellipse = "..."
        return f"{self.message[:cutoff]}{ellipse}"


class PullRequest(models.Model, Mixins):
    OPEN = "open"
    CLOSED = "closed"

    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="pull_requests"
    )

    author_github_name = models.CharField(max_length=100)
    state = models.CharField(max_length=6)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    merged_at = models.DateTimeField(blank=True, null=True)
    number = models.PositiveSmallIntegerField()
    # assignees = ArrayField(models.CharField(max_length=100), default=list)

    # user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # TODO Denormalise (#157)
    class Meta:
        unique_together = [["repository", "number"]]

    @classmethod
    def create_or_update_from_github_api_data(
        cls, repo_full_name, pull_request_data, repo_missing_ok=False
    ):
        from git_real.helpers import strp_github_standard_time

        get_repo = lambda: Repository.objects.get(full_name=repo_full_name)

        if repo_missing_ok:
            try:
                repo = get_repo()
            except Repository.DoesNotExist:
                return
        else:
            repo = get_repo()

        # pr = request_body["pull_request"]
        number = pull_request_data["number"]

        defaults = {
            "state": pull_request_data["state"],
            "title": pull_request_data["title"],
            "body": pull_request_data["body"],
            "created_at": strp_github_standard_time(
                pull_request_data["created_at"],
            ),
            "updated_at": pull_request_data["updated_at"]
            and strp_github_standard_time(
                pull_request_data["updated_at"],
            ),
            "closed_at": pull_request_data["closed_at"]
            and strp_github_standard_time(
                pull_request_data["closed_at"],
            ),
            "merged_at": pull_request_data["merged_at"]
            and strp_github_standard_time(
                pull_request_data["merged_at"],
            ),
        }
        #     "author_github_name": github_user,
        #     "assignees": [d["login"] for d in pr["assignees"]],
        #     "user": get_user_from_github_name(github_user),
        # }
        pull_request, _ = cls.get_or_create_or_update(
            repository=repo, number=number, defaults=defaults, overrides=defaults
        )
        return pull_request


class PullRequestReview(models.Model, Mixins):
    author_github_name = models.CharField(max_length=100)

    pull_request = models.ForeignKey(PullRequest, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(null=True, blank=True)
    body = models.TextField()
    commit_id = models.CharField(max_length=40)
    state = models.CharField(max_length=17)

    number = models.PositiveIntegerField()

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # TODO Denormalise (#157)
