from datetime import timezone
from . import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models import Q
from curriculum_tracking.constants import (
    COMPETENT,
    NOT_YET_COMPETENT,
    RED_FLAG,
    EXCELLENT,
)
from django.utils import timezone

# @receiver([m2m_changed], sender=models.AgileCard.assignees.through)
# def make_sure_project_assignees_match_card(sender, instance, **kwargs):
#     project = instance.recruit_project
#     if project:
#         for user in instance.assignees.all():
#             if user not in project.recruit_users.all():
#                 project.recruit_users.add(user)
#         for user in project.recruit_users.all():
#             if user not in instance.assignees.all():
#                 project.recruit_users.remove(user)


# @receiver([m2m_changed], sender=models.AgileCard.reviewers.through)
# def make_sure_project_reviewers_match_card(sender, instance, **kwargs):
#     project = instance.recruit_project
#     if project:
#         for user in instance.reviewers.all():
#             if user not in project.reviewer_users.all():
#                 project.reviewer_users.add(user)
#         for user in project.reviewer_users.all():
#             if user not in instance.reviewers.all():
#                 project.reviewer_users.remove(user)


# @receiver([m2m_changed], sender=models.RecruitProject.recruit_users.through)
# def make_sure_card_assignees_match_project(sender, instance, **kwargs):
#     try:
#         card = instance.agile_card
#     except models.AgileCard.DoesNotExist:
#         return
#     assert card is not None
#     for user in instance.recruit_users.all():
#         if user not in card.assignees.all():
#             card.assignees.add(user)
#     for user in card.assignees.all():
#         if user not in instance.recruit_users.all():
#             card.assignees.remove(user)


# @receiver([post_save], sender=models.AgileCard)
# def make_sure_card_users_up_to_date_according_to_project(
#     sender, instance, created, **kwargs
# ):
#     # if not created:
#     #     return

#     if instance.recruit_project:
#         for user in instance.recruit_project.recruit_users.all():
#             # if user not in
#             instance.assignees.add(user)
#         for user in instance.recruit_project.reviewer_users.all():
#             instance.reviewers.add(user)
#         for user in instance.assignees.all():
#             if user not in instance.recruit_project.recruit_users.all():
#                 instance.assignees.remove(user)
#         for user in instance.reviewers.all():
#             if user not in instance.recruit_project.reviewer_users.all():
#                 instance.reviewers.remove(user)


@receiver([pre_save], sender=models.RecruitProjectReview)
def set_trusted_on_create(sender, instance, **kwargs):

    if instance.trusted == None:
        instance.trusted = instance.recruit_project.is_trusted_reviewer(
            instance.reviewer_user
        )


@receiver([post_save], sender=models.AgileCard)
def unblock_cards_and_update_complete_time(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if instance.status == models.AgileCard.COMPLETE:
        for card in instance.required_by_cards.filter(status=models.AgileCard.BLOCKED):
            still_needs = card.requires_cards.filter(
                ~Q(status=models.AgileCard.COMPLETE)
            ).count()
            if still_needs == 0:
                card.status = models.AgileCard.READY
                card.save()

        progress_instance = instance.progress_instance
        if progress_instance.__class__ == models.WorkshopAttendance:
            return

        if progress_instance.complete_time == None:
            review = progress_instance.latest_review(trusted=True)
            if review:
                progress_instance.complete_time = review.timestamp
            else:
                progress_instance.complete_time = timezone.now()
            progress_instance.save()

        assert instance.complete_time != None, instance


@receiver([post_save], sender=models.TopicReview)
def maybe_move_card_because_of_topic_review(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        card = models.AgileCard.objects.get(topic_progress=instance.topic_progress)
    except models.AgileCard.DoesNotExist:
        return  # no card to update

    needs_some_work = instance.status in [
        NOT_YET_COMPETENT,
        RED_FLAG,
    ]

    if needs_some_work:
        # move the card back
        card.status = models.AgileCard.REVIEW_FEEDBACK
        card.save()
        return

    assert instance.status in [
        COMPETENT,
        EXCELLENT,
    ], f"Unrecognised status {instance} '{instance.status}''"

    card.status = models.AgileCard.COMPLETE
    card.save()


@receiver([post_save], sender=models.RecruitProjectReview)
def maybe_move_card_because_of_project_review(sender, instance, created, **kwargs):

    if not created:
        return
    try:
        card = models.AgileCard.objects.get(recruit_project=instance.recruit_project)
    except models.AgileCard.DoesNotExist:
        return  # no card to update

    project_needs_some_work = instance.status in [
        NOT_YET_COMPETENT,
        RED_FLAG,
    ]

    if project_needs_some_work:
        # move the card back
        card.status = models.AgileCard.REVIEW_FEEDBACK
        card.save()
        return

    assert instance.status in [
        COMPETENT,
        EXCELLENT,
    ], f"Unrecognised status {instance} '{instance.status}''"

    user_is_trusted = instance.recruit_project.is_trusted_reviewer(
        instance.reviewer_user
    )

    if user_is_trusted:
        recruit_project = instance.recruit_project
        card.status = models.AgileCard.COMPLETE
        card.save()
        recruit_project.complete_time = instance.timestamp
        recruit_project.save()


@receiver([post_save], sender=models.RecruitProjectReview)
def update_project_review_counts(sender, instance, created, **kwargs):
    """whenever a new review is added to a project then update the appropriate review count"""
    if not created:
        return
    instance.update_recent_validation_flags_for_project()
    project = instance.recruit_project

    if instance.status == NOT_YET_COMPETENT:
        project.code_review_ny_competent_since_last_review_request += 1
    elif instance.status == COMPETENT:
        project.code_review_competent_since_last_review_request += 1
    elif instance.status == EXCELLENT:
        project.code_review_excellent_since_last_review_request += 1
    elif instance.status == RED_FLAG:
        project.code_review_red_flag_since_last_review_request += 1
    else:
        raise Exception(f"Unknown status: {instance.status}")
    project.save()


# TODO: adding an assignee or reviewer to card updates the project and vice versa


# @receiver([post_save], sender=models.RecruitProject)
# def update_denorm(sender, instance, **kwargs):
#     if instance.id:
#         l = [str(o.id) for o in instance.recruit_users.all()]
#         recruit_users_str = ",".join(sorted(l))
#         if instance.recruit_users_str != recruit_users_str:
#             instance.recruit_users_str = recruit_users_str
#             instance.save()


# @receiver([post_save], sender=models.AgileCard)
# def update_denorm(sender, instance, **kwargs):
#     if instance.id:
#         l = [str(o.id) for o in instance.assignees.all()]
#         assignees_str = ",".join(sorted(l))
#         if instance.assignees_str != assignees_str:
#             instance.assignees_str = assignees_str
#             instance.save()


# @receiver([post_save], sender=models.AgileCard)
# def update_denorm(sender, instance, **kwargs):
#     def has_recruit_project():
#         if instance.recruit_project:
#             return True

#     def has_reviewers():
#         return bool(instance.reviewers.count())

#     def status_started():
#         return instance.status not in [models.AgileCard.BLOCKED, models.AgileCard.READY]

#     instance.dont_delete = (
#         has_recruit_project() or has_reviewers() or status_started() or False
#     )
