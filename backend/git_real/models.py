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
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    author_github_name = models.CharField(max_length=100)
    state = models.CharField(max_length=6)
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    merged_at = models.DateTimeField(blank=True, null=True)
    number = models.PositiveSmallIntegerField()
    assignees = ArrayField(models.CharField(max_length=100), default=list)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # TODO Denormalise (#157)


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
