# from datetime import timezone
# from . import models
# from django.dispatch import receiver
# from django.db.models.signals import post_save, pre_save
# from django.db.models import Q
# from curriculum_tracking.constants import (
#     COMPETENT,
#     NOT_YET_COMPETENT,
#     RED_FLAG,
#     EXCELLENT,
# )
# from django.utils import timezone
# from django.db.models import Count


# @receiver([post_save], sender=models.PullRequestReview)
# def update_pr_review_validated_flags(sender, instance, created, **kwargs):
#     if not created:
#         return
#     instance.update_recent_validation_flags()
