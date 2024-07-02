from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from core.models import Team
from curriculum_tracking.models import RecruitProject, AgileCard, RecruitProjectReview
from django.utils import timezone
from django.db.models import OuterRef, Exists


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

    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would
            # have pk
            self.due_timestamp = timezone.now() + timedelta(hours=1)
        super(ProjectReviewBundleClaim, self).save(*args, **kwargs)

    @staticmethod
    def get_projects_user_can_review(user):

        reviewed_projects_subquery = RecruitProjectReview.objects.filter(
            recruit_project=OuterRef("recruit_project"),
            reviewer_user=user,
            timestamp__gte=OuterRef("recruit_project__review_request_time"),
        )

        cutoff_datetime = timezone.now() - timedelta(days=1)

        cards = (
            AgileCard.objects.filter(status=AgileCard.IN_REVIEW)
            .filter(assignees__active=True)
            .exclude(content_item__tags__name="technical-assessment")
            .exclude(content_item__tags__name="ncit")
            .exclude(content_item__tags__name="ncba")
            .filter(recruit_project__review_request_time__lte=cutoff_datetime)
            .exclude(
                recruit_project__project_review_bundle_claims__is_active=True
            )  # if the project is already in an active claim, skip it
            .annotate(
                has_reviewed=Exists(reviewed_projects_subquery)
            )  # exclude cards with recent project reviews by user
            .filter(has_reviewed=False)
            .order_by("recruit_project__review_request_time")[:50]  # earliest first
            .prefetch_related("content_item", "recruit_project")
        )

        if user.is_superuser:
            return cards

        viewable_teams = user.get_permissioned_teams(perms=tuple(Team.PERMISSION_VIEW))

        if not len(viewable_teams):
            return []

        permitted_cards = []

        for card in cards:
            assignee = card.assignees.first()
            assignee_teams = assignee.teams_cached()

            if set(viewable_teams).intersection(assignee_teams):
                permitted_cards.append(card)

        return permitted_cards

    def request_user_can_unclaim(self, user=None):
        from threadlocal_middleware import get_current_user

        user = user or get_current_user()

        return self.claimed_by_user == user or user.is_superuser
