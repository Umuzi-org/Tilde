from django.db import models
from curriculum_tracking.constants import POSITIVE_REVIEW_STATUS_CHOICES
from model_mixins import Mixins
from core.models import User
from git_real.helpers import (
    strp_github_standard_time,
    github_timestamp_int_to_tz_aware_datetime,
    get_user_from_github_name,
)

from django.core.exceptions import MultipleObjectsReturned


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

    def get_activity_log_summary_data(self):
        """This is used by the activityLog serializer"""
        # Note: the import direction is wrong. We should not be importing fro curriculum_tracking here. This is technical debt
        from curriculum_tracking.models import AgileCard, RecruitProject

        project = RecruitProject.objects.filter(repository=self).order_by("pk").last()
        card_id = None
        if project:
            try:
                card = project.agile_card
                card_id = card.id
            except AgileCard.DoesNotExist:
                pass

        return {
            "recruit_project": project.id if project else None,
            "card": card_id,
            "title": project.content_item.title if project else None,
            "flavour_names": project.flavour_names if project else None,
        }


class Commit(models.Model, Mixins):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    commit_hash = models.CharField(max_length=40)
    author_github_name = models.CharField(max_length=100)
    author_email = models.CharField(max_length=240)
    message = models.TextField()
    branch = models.CharField(max_length=150)
    datetime = models.DateTimeField()

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

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
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    merged_at = models.DateTimeField(blank=True, null=True)
    number = models.PositiveSmallIntegerField()

    # assignees = ArrayField(models.CharField(max_length=100), default=list)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["repository", "number"]]

    @classmethod
    def create_or_update_from_github_api_data(cls, repo, pull_request_data):
        assert repo != None, "repo is missing"
        number = pull_request_data["number"]

        github_name = pull_request_data["user"]["login"]

        defaults = {
            "state": pull_request_data["state"],
            "title": pull_request_data["title"],
            "body": pull_request_data["body"] or " ",
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
            and strp_github_standard_time(pull_request_data["merged_at"]),
            "author_github_name": github_name,
            "user": get_user_from_github_name(github_name),
        }

        pull_request, _ = cls.get_or_create_or_update(
            repository=repo, number=number, defaults=defaults, overrides=defaults
        )
        return pull_request


class PullRequestReview(models.Model, Mixins):

    CONTRADICTED = "d"

    REVIEW_VALIDATED_STATUS_CHOICES = [
        (CONTRADICTED, "contradicted"),
    ]

    NEGATIVE_STATES = ["changes_requested"]
    POSITIVE_STATES = ["approved"]
    NEUTRAL_STATES = ["commented", "dismissed"]

    html_url = models.CharField(max_length=255, unique=True)
    pull_request = models.ForeignKey(
        PullRequest, on_delete=models.CASCADE, related_name="reviews"
    )
    author_github_name = models.CharField(max_length=100)

    submitted_at = models.DateTimeField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    commit_id = models.CharField(max_length=40)
    state = models.CharField(max_length=17)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    validated = models.CharField(
        choices=REVIEW_VALIDATED_STATUS_CHOICES, max_length=1, null=True, blank=True
    )

    def get_activity_log_summary_data(self):
        """This is used by the activityLog serializer"""
        # Note: the import direction is wrong. We should not be importing fro curriculum_tracking here. This is technical debt
        from curriculum_tracking.models import AgileCard, RecruitProject

        repo = self.pull_request.repository
        project = RecruitProject.objects.filter(repository=repo).order_by("pk").last()
        card_id = None
        if project:
            try:
                card = project.agile_card
                card_id = card.id
            except AgileCard.DoesNotExist:
                pass

        return {
            "recruit_project": project.id if project else None,
            "card": card_id,
            "title": project.content_item.title if project else None,
            "flavour_names": project.flavour_names if project else None,
        }

    def update_recent_validation_flags(self):
        """this review was just created. Update previous reviews"""
        assert (
            len(PullRequestReview.POSITIVE_STATES) == 1
        ), "this function only works if there is one positive state. Upgrade the function"
        state = self.state.lower()
        if state in PullRequestReview.NEGATIVE_STATES:
            prs_to_update = PullRequestReview.objects.filter(
                pull_request=self.pull_request
            ).filter(state__iexact=PullRequestReview.POSITIVE_STATES[0])
            prs_to_update.update(validated=PullRequestReview.CONTRADICTED)

    @classmethod
    def create_or_update_from_github_api_data(cls, pull_request, review_data):
        assert pull_request != None, "repo is missing"

        github_name = review_data["user"]["login"]
        defaults = {
            "body": review_data["body"],
            "commit_id": review_data["commit_id"],
            "state": review_data["state"],
            "submitted_at": review_data.get("submitted_at")
            and strp_github_standard_time(review_data["submitted_at"]),
            "pull_request": pull_request,
            "author_github_name": github_name,
            "user": get_user_from_github_name(github_name),
        }

        try:
            review, _ = cls.get_or_create_or_update(
                html_url=review_data["html_url"], defaults=defaults, overrides=defaults
            )
        except MultipleObjectsReturned:
            reviews = list(cls.objects.filter(html_url=review_data["html_url"]))
            for o in reviews[:-1]:
                o.delete()
            review = reviews[-1]
            review.update(**defaults)
            review.save()

        review.update_recent_validation_flags()
        return review


class Push(models.Model, Mixins):
    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="pushes"
    )
    author_github_name = models.CharField(max_length=100)
    committer_github_name = models.CharField(max_length=100)
    pusher_username = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    head_commit_url = models.CharField(max_length=255)
    commit_timestamp = models.DateTimeField()
    pushed_at_time = models.DateTimeField()
    ref = models.CharField(max_length=255)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["ref", "head_commit_url"]]

    @classmethod
    def create_or_update_from_github_api_data(cls, repo, request_body):

        if request_body["head_commit"] is None and bool(request_body["pusher"]):
            return None
        else:
            pusher_user = request_body.get("pusher").get("name")
            head_commit = request_body["head_commit"]
            head_commit_url = head_commit["url"]
            ref = request_body["ref"]
            defaults = {
                "commit_timestamp": head_commit.get("timestamp"),
                "author_github_name": head_commit.get("author").get("username"),
                "committer_github_name": head_commit.get("committer").get("username"),
                "message": head_commit.get("message"),
                "pusher_username": pusher_user,
                "pushed_at_time": github_timestamp_int_to_tz_aware_datetime(
                    int(request_body["repository"]["pushed_at"])
                ),
                "user": get_user_from_github_name(pusher_user),
            }

            instance, _ = cls.get_or_create_or_update(
                repository=repo,
                head_commit_url=head_commit_url,
                ref=ref,
                defaults=defaults,
                overrides=defaults,
            )
            return instance
