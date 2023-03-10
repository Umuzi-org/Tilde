from django.db import models
from core.models import Curriculum, User
from curriculum_tracking.models import ContentItem, RecruitProject, TopicProgress
from django.db.models import Q
from collections import namedtuple
from curriculum_tracking.constants import RED_FLAG, NOT_YET_COMPETENT

Step = namedtuple("Step", ["content_item", "progress", "status"])


class ChallengeRegistration(models.Model):
    """associates a user with a curriculum"""

    STATUS_DONE = "DONE"
    STATUS_BLOCKED = "BLOCKED"
    STATUS_READY = "READY"
    STATUS_UNDER_REVIEW = "REVIEWING"
    STATUS_ERROR = "ERROR"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="challenge_registrations"
    )
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)
    registration_date = models.DateField(auto_now_add=True)

    class Meta(object):
        unique_together = ["user", "curriculum"]

    def get_steps(self):
        """
        return an ordered list of steps along with their statuses and progress instances

        # TODO: include flavours.
        """
        user = self.user

        def get_progress(item):
            if item.content_type == ContentItem.PROJECT:
                return (
                    RecruitProject.objects.filter(recruit_users=user)
                    .filter(content_item=item)
                    .first()
                )
            if item.content_type == ContentItem.TOPIC:
                return (
                    TopicProgress.objects.filter(user=user)
                    .filter(content_item=item)
                    .first()
                )

        content_items = [
            o.content_item
            for o in self.curriculum.content_requirements.prefetch_related(
                "content_item"
            )
        ]

        progress_entries = [get_progress(item) for item in content_items]

        latest_complete_or_review = -1
        latest_status = ""
        for i, p in enumerate(progress_entries):
            if p == None:
                break
            if p.complete_time:
                latest_complete_or_review = i
                latest_status = ChallengeRegistration.STATUS_DONE
            elif p.review_request_time:
                latest_complete_or_review = i
                has_error = (
                    p.project_reviews.filter(timestamp__gte=p.review_request_time)
                    .filter(Q(status=NOT_YET_COMPETENT) | Q(status=RED_FLAG))
                    .count()
                )

                latest_status = (
                    ChallengeRegistration.STATUS_ERROR
                    if has_error
                    else ChallengeRegistration.STATUS_UNDER_REVIEW
                )
            else:
                break

        def get_status(index):
            if index < latest_complete_or_review:
                return self.STATUS_DONE
            if index == latest_complete_or_review:
                return latest_status
            if index == latest_complete_or_review + 1:
                if latest_status == self.STATUS_DONE:
                    return self.STATUS_READY
                else:
                    return self.STATUS_BLOCKED

            return self.STATUS_BLOCKED

        return [
            Step(content_item=content_item, progress=progress, status=get_status(index))
            for index, (content_item, progress) in enumerate(
                zip(content_items, progress_entries)
            )
        ]
