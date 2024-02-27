from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from curriculum_tracking.models import RecruitProject
from django.utils import timezone


User = get_user_model()


class ProjectReviewBundleClaim(models.Model):
    claimed_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    claim_timestamp = models.DateTimeField(auto_now_add=True)
    due_timestamp = models.DateTimeField()
    projects_to_review = models.ManyToManyField(
        RecruitProject, related_name="project_review_bundle_claims"
    )
    projects_reviewed = models.ManyToManyField(
        RecruitProject,
        related_name="project_review_bundle_claims_reviewed",
    )

    projects_someone_else_got_to = models.ManyToManyField(RecruitProject)

    is_active = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.due_timestamp = timezone.now() + timedelta(hours=1)
