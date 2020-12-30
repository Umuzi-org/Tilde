from rest_framework.permissions import BasePermission
from . import models
from git_real import models as git_models


class IsProjectAssignee(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project = view.get_object()
        return user in project.recruit_users.all()


class IsTopicProgressUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        topic_progress = view.get_object()
        return topic_progress.user == user


class IsProjectReviewer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        project = view.get_object()
        return user in project.reviewer_users.all()


class IsCurrentUserInUsersForFilteredTopicProgress(BasePermission):
    def has_permission(self, request, view):
        if request.method != "GET":
            return False
        if "topic_progress" not in request.GET:
            return False
        topic_progress = models.TopicProgress.objects.get(
            pk=int(request.GET["topic_progress"])
        )
        return request.user == topic_progress.user


# class IsCurrentUserInReviewersForFilteredTopicProgress(BasePermission):
#     def has_permission(self, request, view):
#         if request.method != "GET":
#             return False
#         if "recruit_project" not in request.GET:
#             return False
#         project = models.RecruitProject.objects.get(
#             pk=int(request.GET["recruit_project"])
#         )
#         return request.user in project.reviewer_users.all()


class IsCurrentUserInRecruitsForFilteredProject(BasePermission):
    def has_permission(self, request, view):
        if request.method != "GET":
            return False
        if "recruit_project" not in request.GET:
            return False
        project = models.RecruitProject.objects.get(
            pk=int(request.GET["recruit_project"])
        )
        return request.user in project.recruit_users.all()


class IsCurrentUserInReviewersForFilteredProject(BasePermission):
    def has_permission(self, request, view):
        if request.method != "GET":
            return False
        if "recruit_project" not in request.GET:
            return False
        project = models.RecruitProject.objects.get(
            pk=int(request.GET["recruit_project"])
        )
        return request.user in project.reviewer_users.all()


class IsCardAssignee(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        card = view.get_object()
        return user in card.assignees.all()


class IsCardReviewer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        card = view.get_object()
        return user in card.reviewers.all()


def user_can_see_repository(repo, user):
    for project in repo.recruit_projects.all():
        if user in project.recruit_users.all():
            return True
        if user in project.reviewer_users.all():
            return True
    return False


class IsRepoAttachedToProjectICanSee(BasePermission):
    def has_permission(self, request, view):
        repo = view.get_object()
        user = request.user
        return user_can_see_repository(repo, user)


class IsFilteredByRepoAttachedToProjectICanSee(BasePermission):
    """what a mouthful"""

    def has_permission(self, request, view):
        if request.method != "GET":
            return False
        if "repository" not in request.GET:
            return False
        repo = git_models.Repository.objects.get(pk=int(request.GET["repository"]))
        user = request.user

        return user_can_see_repository(repo, user)


class CardCanStart(BasePermission):
    def has_permission(self, request, view):
        card = view.get_object()
        return card.can_start()


class CardCanForceStart(BasePermission):
    def has_permission(self, request, view):
        card = view.get_object()
        return card.can_start(force=True)


class CardDueTimeIsNotSet(BasePermission):
    def has_permission(self, request, view):
        card = view.get_object()
        if card.content_item.content_type == models.ContentItem.PROJECT:
            progress = card.recruit_project
        elif card.content_item.content_type == models.ContentItem.TOPIC:
            progress = card.topic_progress
        else:
            raise NotImplementedError(
                f"Unrecognised card type: {models.ContentItem.content_type}"
            )

        if not progress:
            return True
        return progress.due_time == None


class CardBelongsToRequestingUser(BasePermission):
    def has_permission(self, request, view):
        if "pk" not in view.kwargs:
            return False
        card = view.get_object()
        user = request.user
        if user in card.assignees.all():
            return True
        if user in card.reviewers.all():
            return True
        return False


# def IsGroupManager(group_id_field):
#     class _IsGroupManager(BasePermission):
#         def has_permission(self, request, view):

#             # if len(request.query_params) == 0:
#             #     return True
#             user = request.user
#             print(group_id_field)
#             # filter_by = dict(request.query_params).get(filter_name, [])

#             breakpoint()
#             todo

#     return _IsGroupManager


# def IsUserManager(user_id_field):
#     class _IsUserManager(BasePermission):
#         def has_permission(self, request, view):
#             user = request.user
#             breakpoint()
#             todo

#     return _IsUserManager


class IsWorkshopAttendee(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        workshop_attendance = view.get_object()
        return workshop_attendance.attendee_user == user
