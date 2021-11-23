from . import models
from rest_framework import serializers


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repository
        fields = [
            "id",
            "owner",
            "full_name",
            "ssh_url",
            "created_at",
            "private",
            "archived",
            "user",
        ]


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Commit
        fields = [
            "id",
            "repository",
            "commit_hash",
            "author_github_name",
            "author_email",
            "message",
            "branch",
            "datetime",
            "user",
        ]


class PullRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PullRequest
        fields = [
            "id",
            "repository",
            "author_github_name",
            "state",
            "title",
            "body",
            "created_at",
            "updated_at",
            "closed_at",
            "merged_at",
            "number",
            # "assignees",
            # "user",
        ]


class PullRequestReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PullRequestReview
        fields = [
            "id",
            "author_github_name",
            "pull_request",
            "submitted_at",
            "body",
            "commit_id",
            "state",
            # "number",
            "user",
        ]

class PushSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Push
        fields = [
            "id",
            "repository",
            "author_github_name",
            "committer_github_name",
            "pusher_username",
            "message",
            "head_commit_url",
            "commit_timestamp",
            "pushed_at_time",
            "ref",
        ]
