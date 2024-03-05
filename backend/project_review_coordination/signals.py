from curriculum_tracking.models import RecruitProjectReview
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ProjectReviewBundleClaim
from curriculum_tracking.constants import (
    COMPETENT,
    NOT_YET_COMPETENT,
    RED_FLAG,
    EXCELLENT,
)


@receiver([post_save], sender=RecruitProjectReview)
def update_claims(sender, instance, created, **kwargs):

    if not created:
        return

    project = instance.recruit_project

    reviewer_user_claims = (
        ProjectReviewBundleClaim.objects.filter(claimed_by_user=instance.reviewer_user)
        .filter(is_active=True)
        .filter(projects_to_review=project)
    )

    for claim in reviewer_user_claims:
        claim.projects_to_review.remove(project)
        claim.projects_reviewed.add(project)

        if claim.projects_to_review.count() == 0:
            claim.is_active = False
            claim.save()

    # if someone moved a card and it no longer needs a review then update the claim as well
    # this would be done if the project received a negative review or a trusted positive review
    is_closing_review = project.is_trusted_reviewer(
        instance.reviewer_user
    ) and instance.status in [COMPETENT, EXCELLENT]
    is_negative_review = instance.status in [NOT_YET_COMPETENT, RED_FLAG]

    if is_closing_review or is_negative_review:
        # closing review. Update the claim
        claims = ProjectReviewBundleClaim.objects.filter(is_active=True).filter(
            projects_to_review=project
        )

        for claim in claims:
            claim.projects_to_review.remove(project)
            claim.projects_someone_else_got_to.add(project)

            if claim.projects_to_review.count() == 0:
                claim.is_active = False
                claim.save()
