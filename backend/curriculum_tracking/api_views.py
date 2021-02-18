from git_real import models as git_models
from git_real import serializers as git_serializers
from django.utils import timezone
from django.http import Http404, HttpResponseForbidden
from rest_framework.decorators import action
from curriculum_tracking import permissions as curriculum_permissions
from core import permissions as core_permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from . import serializers
from . import models
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets, status
from core.permissions import (
    ActionIs,
    IsStaffUser,
    HasObjectPermission,
    IsReadOnly,
    DenyAll,
)
from core.models import Team

User = get_user_model()


def _get_teams_from_topic_progress(self, request, view):
    topic_progress = view.get_object()
    return _get_teams_from_topic_progress_instance(topic_progress)


def _get_teams_from_topic_progress_instance(topic_progress):
    user_ids = [topic_progress.user.id]
    # user_ids = [user.id for user in project.recruit_users.all()]
    return Team.get_teams_from_user_ids(user_ids)


def _get_teams_from_recruit_project(self, request, view):
    project = view.get_object()
    return project.get_teams()
    # return _get_teams_from_recruit_project_instance(project)


# def _get_teams_from_recruit_project_instance(project):


def _get_teams_from_recruit_project_review(self, request, view):
    project_review = view.get_object()
    project = project_review.project
    user_ids = [user.id for user in project.recruit_users.all()] + [
        project_review.reviewer_user_id
    ]
    return Team.get_teams_from_user_ids(user_ids)


def _get_teams_from_topic_review(self, request, view):
    review = view.get_object()
    user_ids = [review.topic_progress.user.id, review.reviewer_user.id]
    return Team.get_teams_from_user_ids(user_ids)


def _get_teams_from_card(self, request, view):
    card = view.get_object()
    user_ids = [user.id for user in card.assignees.all()]
    user_ids += [user.id for user in card.reviewers.all()]
    return Team.get_teams_from_user_ids(user_ids)


def _get_teams_from_recruit_project_filter(self, request, view):
    recruit_project_id = dict(request.query_params).get("recruit_project", [0])
    if len(recruit_project_id) > 1:
        raise Exception("Not Implemented")
    recruit_project_id = recruit_project_id[0]
    if recruit_project_id == 0:
        return []
    try:
        project = models.RecruitProject.objects.get(pk=recruit_project_id)
    except models.RecruitProject.DoesNotExist:
        return []
    return project.get_teams()


def _get_teams_from_topic_progress_filter(self, request, view):
    topic_progress_id = dict(request.query_params).get("topic_progress", [0])
    if len(topic_progress_id) > 1:
        raise Exception("Not Implemented")
    topic_progress_id = topic_progress_id[0]
    if topic_progress_id == 0:
        return []
    try:
        topic_progress = models.TopicProgress.objects.get(pk=topic_progress_id)
    except models.TopicProgress.DoesNotExist:
        return []
    return _get_teams_from_topic_progress_instance(topic_progress)


def _get_teams_from_user_filter(filter_name):
    def get_teams_from_user_filter(self, request, view):
        user_ids = core_permissions.get_clean_user_ids_from_filter(request, filter_name)
        return Team.get_teams_from_user_ids(user_ids)

    return get_teams_from_user_filter


def _get_teams_from_repository_instance(repo):
    projects = repo.recruit_projects.all()
    for project in projects:
        user_ids = [user.id for user in project.recruit_users.all()]
        for team in Team.get_teams_from_user_ids(user_ids):
            yield team


def _get_teams_from_repository(self, request, view):
    repo = view.get_object()
    return _get_teams_from_repository_instance(repo)


def _get_teams_from_repository_filter(self, request, view):
    repo_id = dict(request.query_params).get("repository")
    if not repo_id:
        return ()
    if type(repo_id) is list:
        assert len(repo_id) == 1
        repo = git_models.Repository.objects.get(pk=repo_id[0])
    else:
        repo = git_models.Repository.objects.get(pk=repo_id)

    return _get_teams_from_repository_instance(repo)


def _get_teams_from_workshop_attendance(self, request, view):
    attendance = view.get_object()
    user_ids = [attendance.attendee_user_id]
    return Team.get_teams_from_user_ids(user_ids=user_ids)


from django.db.models import Q

from rest_framework import filters


class CardSummaryViewset(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAdminUser
        | core_permissions.ActionIs("retrieve")
        & (
            curriculum_permissions.IsCardAssignee
            | curriculum_permissions.IsCardReviewer
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW, get_objects=_get_teams_from_card
            )
        )
        | core_permissions.IsReadOnly
        | core_permissions.IsStaffUser
        | core_permissions.IsCurrentUserInSpecificFilter("assignees")
        | core_permissions.HasObjectPermission(
            permissions=Team.PERMISSION_VIEW,
            get_objects=_get_teams_from_user_filter("assignees"),
        ),
    ]
    serializer_class = serializers.cardsummarySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["assignees", "content_item__content_type", "status"]

    ordering_fields = ["recruit_project__complete_time"]

    queryset = (
        models.AgileCard.objects.order_by("order")
        .filter(
            Q(content_item__content_type=models.ContentItem.PROJECT)
            | Q(content_item__topic_needs_review=True)
        )
        .prefetch_related("content_item")
        .prefetch_related("recruit_project")
    )


#     def get_permissions(self):
#         # curriculum_permissions.IsCurrentUserInRecruitsForFilteredProject
#         #     | curriculum_permissions.IsCurrentUserInReviewersForFilteredProject
#         breakpoint()
#         foo
#         o = PermissionClass()
#         o.has_permission(view=self, request=self.request)
#         """
#         curl 'http://127.0.0.1:8000/api/card_summaries/3/' \
#   -H 'Connection: keep-alive' \
#   -H 'Pragma: no-cache' \
#   -H 'Cache-Control: no-cache' \
#   -H 'Authorization: Token e27297adb4c35d54f5bec3125a92cc48f783899c' \
#   -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36' \
#   -H 'Content-Type: application/json' \
#   -H 'Accept: */*' \
#   -H 'Origin: http://localhost:3000' \
#   -H 'Sec-Fetch-Site: cross-site' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Accept-Language: en-US,en;q=0.9' \
#   --compressed
#         """
#         return super().get_permissions()


class AgileCardViewset(viewsets.ModelViewSet):

    serializer_class = serializers.AgileCardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["assignees", "reviewers", "status"]

    queryset = models.AgileCard.objects.order_by("order").prefetch_related(
        "recruit_project"
    )

    permission_classes = [
        (
            core_permissions.ActionIs("retrieve")
            & (
                curriculum_permissions.CardBelongsToRequestingUser
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=_get_teams_from_card,
                )
            )
        )
        | (
            core_permissions.ActionIs("list")
            & (
                core_permissions.IsCurrentUserInSpecificFilter("assignees")
                | core_permissions.IsCurrentUserInSpecificFilter("reviewers")
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=_get_teams_from_user_filter("assignees"),
                )
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=_get_teams_from_user_filter("reviewers"),
                )
            )
        )
    ]

    def get_card_or_error(self, status_or_404, type_or_404):
        card = self.get_object()
        if status_or_404 and card.status != status_or_404:
            raise Http404()
        if card.content_type != type_or_404:
            raise Http404()

        return card

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.SetDueTimeSerializer,
        permission_classes=[
            (
                curriculum_permissions.IsCardAssignee
                & curriculum_permissions.CardDueTimeIsNotSet
            )
            | IsStaffUser
            | HasObjectPermission(
                permissions=Team.PERMISSION_MANAGE_CARDS,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def set_card_due_time(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            card = self.get_object()
            card.set_due_time(serializer.data["due_time"])

            return Response(serializers.AgileCardSerializer(card).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(
    #     detail=True,
    #     methods=["post"],
    #     serializer_class=serializers.AddReviewerUserSerializer,
    #     permission_classes=[permissions.IsAdminUser | core_permissions.IsStaffUser],
    # )
    # def add_reviewer(self, request, pk=None):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         TODO
    #         return Response(serializers.AgileCardSerializer(card).data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NewReviewSerializer,
        permission_classes=[
            curriculum_permissions.IsCardReviewer
            | HasObjectPermission(
                permissions=Team.PERMISSION_REVIEW_CARDS,
                get_objects=_get_teams_from_card,
            )
            | HasObjectPermission(
                permissions=Team.PERMISSION_TRUSTED_REVIEWER,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def add_review(self, request, pk=None):

        # TODO: Debounce or rate limit
        card = self.get_object()
        # breakpoint()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if card.content_item.content_type == models.ContentItem.PROJECT:
                if card.recruit_project == None:
                    raise Http404

                models.RecruitProjectReview.objects.create(
                    status=serializer.data["status"],
                    timestamp=timezone.now(),
                    comments=serializer.data["comments"],
                    recruit_project=card.recruit_project,
                    reviewer_user=request.user,
                )
            elif card.content_item.content_type == models.ContentItem.TOPIC:
                if card.topic_progress == None:
                    raise Http404

                models.TopicReview.objects.create(
                    status=serializer.data["status"],
                    timestamp=timezone.now(),
                    comments=serializer.data["comments"],
                    topic_progress=card.topic_progress,
                    reviewer_user=request.user,
                )

            card.refresh_from_db()
            return Response(serializers.AgileCardSerializer(card).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            curriculum_permissions.IsCardAssignee
            | HasObjectPermission(
                permissions=Team.PERMISSION_MANAGE_CARDS,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def request_review(self, request, pk=None):
        card: models.AgileCard = self.get_object()
        if card.recruit_project:
            card.recruit_project.request_review(force_timestamp=timezone.now())
        elif card.topic_progress:
            card.finish_topic()
        else:
            raise Http404
        card.refresh_from_db()
        assert (
            card.status == models.AgileCard.IN_REVIEW
        ), f"Expected to be in review, but got {card.status}"
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            curriculum_permissions.IsCardAssignee
            | HasObjectPermission(
                permissions=Team.PERMISSION_MANAGE_CARDS,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def cancel_review_request(self, request, pk=None):
        card = self.get_object()
        if card.status != models.AgileCard.IN_REVIEW:
            raise Http404()
        if card.recruit_project:
            card.recruit_project.cancel_request_review()
        elif card.topic_progress:
            card.topic_progress.cancel_request_review()

        # card.status = models.AgileCard.IN_PROGRESS
        # card.save()
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            (
                curriculum_permissions.IsCardAssignee
                & curriculum_permissions.CardCanStart
            )
            | (
                HasObjectPermission(
                    permissions=Team.PERMISSION_MANAGE_CARDS,
                    get_objects=_get_teams_from_card,
                )
                & curriculum_permissions.CardCanForceStart
            ),
        ],
    )
    def start_project(self, request, pk=None):
        card: models.AgileCard = self.get_card_or_error(
            status_or_404=None,
            type_or_404=models.ContentItem.PROJECT,
        )
        card.start_project()
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.ProjectSubmitLink,
        permission_classes=[
            curriculum_permissions.IsCardAssignee
            | HasObjectPermission(
                permissions=Team.PERMISSION_MANAGE_CARDS,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def set_project_link(self, request, pk=None):
        card = self.get_card_or_error(
            status_or_404=None,
            type_or_404=models.ContentItem.PROJECT,
        )
        content_item = card.content_item
        assert (
            content_item.project_submission_type == content_item.LINK
        ), "Cannot submit a link for project with submision type: {content_item.project_submission_type}\n\tcard={card}"

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            card.recruit_project.link_submission = serializer.data["link_submission"]
            card.recruit_project.save()
            card.refresh_from_db()
            return Response(serializers.AgileCardSerializer(card).data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            (
                curriculum_permissions.IsCardAssignee
                & curriculum_permissions.CardCanStart
            )
            | (
                HasObjectPermission(
                    permissions=Team.PERMISSION_MANAGE_CARDS,
                    get_objects=_get_teams_from_card,
                )
                & curriculum_permissions.CardCanForceStart
            ),
        ],
    )
    def start_topic(self, request, pk=None):
        card = self.get_card_or_error(
            status_or_404=models.AgileCard.READY, type_or_404=models.ContentItem.TOPIC
        )
        if not card.can_start():
            raise HttpResponseForbidden()
        card.start_topic()
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            curriculum_permissions.IsCardAssignee
            | HasObjectPermission(
                permissions=Team.PERMISSION_MANAGE_CARDS,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def stop_topic(self, request, pk=None):
        card = self.get_card_or_error(
            status_or_404=models.AgileCard.IN_PROGRESS,
            type_or_404=models.ContentItem.TOPIC,
        )
        card.stop_topic()
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            curriculum_permissions.IsCardAssignee
            | HasObjectPermission(
                permissions=Team.PERMISSION_MANAGE_CARDS,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def finish_topic(self, request, pk=None):
        card = self.get_card_or_error(
            status_or_404=models.AgileCard.IN_PROGRESS,
            type_or_404=models.ContentItem.TOPIC,
        )

        card.finish_topic()
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            HasObjectPermission(
                permissions=Team.PERMISSION_MANAGE_CARDS,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def mark_workshop_attendance(self, request, pk=None):

        card = self.get_card_or_error(
            status_or_404=None, type_or_404=models.ContentItem.WORKSHOP
        )
        card.attended_workshop(timestamp=timezone.now())
        return Response(serializers.AgileCardSerializer(card).data)
        # serializer = self.get_serializer(data=request.data)

        # if serializer.is_valid():
        #     card.attended_workshop(timestamp = serializer.data['timestamp'])
        #     return Response(serializers.AgileCardSerializer(card).data)
        # else:
        #     return Response(serializer.errors,
        #                     status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            HasObjectPermission(
                permissions=Team.PERMISSION_MANAGE_CARDS,
                get_objects=_get_teams_from_card,
            )
        ],
    )
    def cancel_workshop_attendance(self, request, pk=None):
        card = self.get_card_or_error(
            status_or_404=models.AgileCard.COMPLETE,
            type_or_404=models.ContentItem.WORKSHOP,
        )
        card.delete_workshop_attendance()
        return Response(serializers.AgileCardSerializer(card).data)

    # def todo_content_in_ready_column(self):
    #     todo_tag, _ = taggit.models.Tag.objects.get_or_create(name="todo")
    #     AgileCard.objects.filter(status=AgileCard.READY).filter(content_item__tags__in=[todo_tag]).values('content_item','content_item__title','content_item__content_type').distinct()

    # def workshop_content_in_ready_column(self):
    #     AgileCard.objects.filter(status=AgileCard.READY).filter(content_item__content_type=ContentItem.WORKSHOP).values('content_item','content_item__title').distinct()


class RecruitProjectViewset(viewsets.ModelViewSet):  # TODO

    serializer_class = serializers.RecruitProjectSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["recruit_users", "reviewer_users"]

    queryset = models.RecruitProject.objects.order_by("pk").prefetch_related(
        "agile_card", "content_item"
    )

    def get_permissions(self):
        # breakpoint()

        # o = core_permissions.HasObjectPermission(
        #     Team.PERMISSION_VIEW,
        #     _get_teams_from_user_filter("recruit_users"),
        # )()
        # o.has_permission(view=self, request=self.request)

        # wooo
        permission_classes = [IsReadOnly]
        if self.action == "retrieve":
            permission_classes = [
                curriculum_permissions.IsProjectAssignee
                | curriculum_permissions.IsProjectReviewer
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=_get_teams_from_recruit_project,
                )
            ]
        elif self.action == "list":
            permission_classes = [
                core_permissions.IsCurrentUserInSpecificFilter("recruit_users")
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=_get_teams_from_user_filter("recruit_users"),
                )
            ]
        return [permission() for permission in permission_classes]


class TopicProgressViewset(viewsets.ModelViewSet):
    serializer_class = serializers.TopicProgressSerializer
    queryset = models.TopicProgress.objects.order_by("pk")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]

    def get_permissions(self):
        permission_classes = [IsReadOnly]
        if self.action == "retrieve":
            permission_classes = [
                curriculum_permissions.IsTopicProgressUser
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=_get_teams_from_topic_progress,
                )
            ]
        elif self.action == "list":
            permission_classes = [
                core_permissions.IsCurrentUserInSpecificFilter("user")
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=_get_teams_from_user_filter("user"),
                )
            ]

        return [permission() for permission in permission_classes]


class TopicReviewViewset(viewsets.ModelViewSet):
    serializer_class = serializers.TopicReviewSerializer
    queryset = models.TopicReview.objects.order_by("pk")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "status",
        "reviewer_user",
        "topic_progress",
        "topic_progress__user",
    ]

    permission_classes = [
        ActionIs("list")
        & (
            curriculum_permissions.IsCurrentUserInUsersForFilteredTopicProgress
            | curriculum_permissions.IsCurrentUserInReviewersForFilteredTopicProgress
            | core_permissions.IsCurrentUserInSpecificFilter("reviewer_user")
            | core_permissions.IsCurrentUserInSpecificFilter("topic_progress__user")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_user_filter("topic_progress__user"),
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_user_filter("reviewer_user"),
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_topic_progress_filter,
            )
        )
        | ActionIs("retrieve")
        & (
            curriculum_permissions.IsCurrentUserInUsersForFilteredTopicProgress
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_topic_review,
            )
        )
    ]


class RecruitProjectReviewViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RecruitProjectReviewSerializer
    queryset = models.RecruitProjectReview.objects.order_by("-timestamp")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "status",
        "reviewer_user",
        "recruit_project",
        "recruit_project__recruit_users",
    ]

    permission_classes = [
        ActionIs("list")
        & (
            curriculum_permissions.IsCurrentUserInRecruitsForFilteredProject
            | curriculum_permissions.IsCurrentUserInReviewersForFilteredProject
            | core_permissions.IsCurrentUserInSpecificFilter("reviewer_user")
            | core_permissions.IsCurrentUserInSpecificFilter(
                "recruit_project__recruit_users"
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_user_filter(
                    "recruit_project__recruit_users"
                ),
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_user_filter("reviewer_user"),
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_recruit_project_filter,
            )
        )
        | ActionIs("retrieve")
        & (
            # curriculum_permissions.IsCurrentUserInRecruitsForFilteredProject
            # | curriculum_permissions.IsCurrentUserInReviewersForFilteredProject
            core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_recruit_project_review,
            )
        )
    ]

    # def get_permissions(self):
    #     breakpoint()
    #     foo

    #     o = PermissionClass()
    #     o.has_permission(view=self, request=self.request)
    #     return super().get_permissions()


class ContentItemViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ContentItemSerializer
    queryset = models.ContentItem.objects.order_by("pk")

    permission_classes = [IsReadOnly]


class ContentItemOrderViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ContentItemOrderSerializer
    queryset = models.ContentItemOrder.objects.order_by("pk")
    permission_classes = [IsReadOnly]


class RepositoryViewset(viewsets.ModelViewSet):
    serializer_class = git_serializers.RepositorySerializer
    queryset = git_models.Repository.objects.all()

    permission_classes = [
        ActionIs("retrieve")
        & (
            curriculum_permissions.IsRepoAttachedToProjectICanSee
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_repository,
            )
        )
        | ActionIs("list") & (permissions.IsAdminUser)
    ]


class CommitViewSet(viewsets.ModelViewSet):
    serializer_class = git_serializers.CommitSerializer
    queryset = git_models.Commit.objects.order_by("-datetime")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["repository"]

    permission_classes = [
        ActionIs("list")
        & (
            curriculum_permissions.IsFilteredByRepoAttachedToProjectICanSee
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_repository_filter,
            )
        )
    ]


class PullRequestViewSet(viewsets.ModelViewSet):
    serializer_class = git_serializers.PullRequestSerializer
    queryset = git_models.PullRequest.objects.order_by("-created_at")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["repository"]

    permission_classes = [
        ActionIs("list")
        & (
            curriculum_permissions.IsFilteredByRepoAttachedToProjectICanSee
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_repository_filter,
            )
        )
    ]


class PullRequestReviewViewSet(viewsets.ModelViewSet):
    serializer_class = git_serializers.PullRequestReviewSerializer
    queryset = git_models.PullRequestReview.objects.order_by("-submitted_at")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["pull_request"]

    permission_classes = [DenyAll]  # this viewset might not be needed...


class WorkshopAttendanceViewset(viewsets.ModelViewSet):

    serializer_class = serializers.WorkshopAttendanceSerializer
    queryset = models.WorkshopAttendance.objects.order_by("pk")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["attendee_user"]

    permission_classes = [
        ActionIs("retrieve")
        & (
            curriculum_permissions.IsWorkshopAttendee
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_workshop_attendance,
            )
        )
        | ActionIs("list")
        & (
            core_permissions.IsCurrentUserInSpecificFilter("attendee_user")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_user_filter("attendee_user"),
            )
        )
    ]


class ManagmentActionsViewSet(viewsets.ViewSet):
    serializer_class = serializers.NoArgs

    def list(self, request):
        return Response([])

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.GroupSelfReviewSerialiser,
        permission_classes=[permissions.IsAdminUser],  # TODO
    )
    def team_shuffle_review_self(self, request, pk=None):
        """randomise group members and assign them as reviewers to each others cards for a specific project"""
        if request.method == "get":
            return Response({"status": "OK"})
        from long_running_request_actors import team_shuffle_review_self as actor

        response = actor.send(
            team_id="todo", flavour_names="todo", content_item_id="todo"
        )
        return Response({"status": "OK", "data": response.asdict()})

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.TeamReviewByOtherSerialiser,
        permission_classes=[DenyAll],  # TODO
    )
    def team_review_by_other(self, request, pk=None):
        """grab users from another group and randomise them as reviewers for this group"""
        todo

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.TeamReviewByUserSerialiser,
        permission_classes=[DenyAll],  # TODO
    )
    def assign_user_as_reviewer(self, request, pk=None):
        todo

    # TODO: bulk set due dates