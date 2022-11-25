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
from rest_framework.response import Response
from rest_framework import viewsets, status
from core.permissions import (
    ActionIs,
    IsStaffUser,
    HasObjectPermission,
    IsReadOnly,
    DenyAll,
    IsCurrentUserInSpecificFilter,
)
from core.models import Team, User, Stream
import curriculum_tracking.activity_log_entry_creators as log_creators
from rest_framework import filters
from social_auth.models import SocialProfile
from guardian.shortcuts import get_objects_for_user
from django.db.models import Q, Max
from django.db.models import Count
from sql_util.utils import SubqueryAggregate
from core import serializers as core_serializers


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
            get_objects=core_permissions.get_teams_from_user_filter("assignees"),
        ),
    ]
    serializer_class = serializers.CardSummarySerializer
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


class AgileCardViewset(viewsets.ModelViewSet):

    serializer_class = serializers.AgileCardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["assignees", "reviewers", "status", "requires_cards"]

    queryset = (
        models.AgileCard.objects.order_by("order")
        .prefetch_related("recruit_project")
        .prefetch_related("recruit_project__repository__pull_requests")
    )

    permission_classes = [
        (
            core_permissions.ActionIs("retrieve")
            & (
                curriculum_permissions.CardBelongsToRequestingUser
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW, get_objects=_get_teams_from_card
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
                    get_objects=core_permissions.get_teams_from_user_filter(
                        "assignees"
                    ),
                )
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=core_permissions.get_teams_from_user_filter(
                        "reviewers"
                    ),
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
        card = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if card.content_item.content_type == models.ContentItem.PROJECT:
                if card.recruit_project == None:
                    raise Http404

                review = models.RecruitProjectReview.objects.create(
                    status=serializer.data["status"],
                    timestamp=timezone.now(),
                    comments=serializer.data["comments"],
                    recruit_project=card.recruit_project,
                    reviewer_user=request.user,
                )
                log_creators.log_project_competence_review_done(review)

            elif card.content_item.content_type == models.ContentItem.TOPIC:
                if card.topic_progress == None:
                    raise Http404

                review = models.TopicReview.objects.create(
                    status=serializer.data["status"],
                    timestamp=timezone.now(),
                    comments=serializer.data["comments"],
                    topic_progress=card.topic_progress,
                    reviewer_user=request.user,
                )

                log_creators.log_topic_competence_review_done(review)

            card.refresh_from_db()
            if card.status == models.AgileCard.REVIEW_FEEDBACK:
                log_creators.log_card_moved_to_review_feedback(card, request.user)
            elif card.status == models.AgileCard.COMPLETE:
                log_creators.log_card_moved_to_complete(card, request.user)

            return Response(serializers.AgileCardSerializer(card).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=core_serializers.NoArgs,
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

        log_creators.log_card_review_requested(card=card, actor_user=request.user)

        card.refresh_from_db()
        assert (
            card.status == models.AgileCard.IN_REVIEW
        ), f"Expected to be in review, but got {card.status}"
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=core_serializers.NoArgs,
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

        log_creators.log_card_review_request_cancelled(
            card=card, actor_user=request.user
        )
        card.refresh_from_db()
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=core_serializers.NoArgs,
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
            )
        ],
    )
    def start_project(self, request, pk=None):
        card: models.AgileCard = self.get_card_or_error(
            status_or_404=None, type_or_404=models.ContentItem.PROJECT
        )
        card.start_project()

        log_creators.log_card_started(card=card, actor_user=request.user)

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
            status_or_404=None, type_or_404=models.ContentItem.PROJECT
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
        serializer_class=core_serializers.NoArgs,
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
            )
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
        serializer_class=core_serializers.NoArgs,
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
        serializer_class=core_serializers.NoArgs,
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
        serializer_class=core_serializers.NoArgs,
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
        serializer_class=core_serializers.NoArgs,
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
        #     core_permissions.get_teams_from_user_filter("recruit_users"),
        # )()
        # o.has_permission(view=self, request=self.request)

        # wooo
        permission_classes = [IsReadOnly]
        if self.action == "retrieve":
            permission_classes = [
                permissions.IsAdminUser
                | curriculum_permissions.IsProjectAssignee
                | curriculum_permissions.IsProjectReviewer
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=_get_teams_from_recruit_project,
                )
            ]
        elif self.action == "list":
            permission_classes = [
                permissions.IsAdminUser
                | core_permissions.IsCurrentUserInSpecificFilter("recruit_users")
                | core_permissions.HasObjectPermission(
                    permissions=Team.PERMISSION_VIEW,
                    get_objects=core_permissions.get_teams_from_user_filter(
                        "recruit_users"
                    ),
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
                    get_objects=core_permissions.get_teams_from_user_filter("user"),
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
                get_objects=core_permissions.get_teams_from_user_filter(
                    "topic_progress__user"
                ),
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter(
                    "reviewer_user"
                ),
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


class PullRequestReviewQualityViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PullRequestReviewQualitySerializer
    queryset = (
        git_models.PullRequestReview.objects.order_by("-submitted_at")
        .annotate(
            project_count=SubqueryAggregate(
                "pull_request__repository__recruit_projects", aggregate=Count
            )
        )
        .filter(project_count__gte=1)
    )

    # .filter_by(repository__recruit_projects)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "submitted_at": ["gte", "lte"],
        "user": ["exact"],
    }
    permission_classes = [
        ActionIs("list")
        & (
            curriculum_permissions.IsCurrentUserInRecruitsForFilteredProject
            | curriculum_permissions.IsCurrentUserInReviewersForFilteredProject
            | core_permissions.IsCurrentUserInSpecificFilter("reviewer_user")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter(
                    "reviewer_user"
                ),
            )
        )
        | ActionIs("retrieve")
        & (
            core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_recruit_project_review,
            )
        )
    ]


class RecruitProjectReviewQualityViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RecruitProjectReviewQualitySerializer
    queryset = models.RecruitProjectReview.objects.order_by("-timestamp")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "timestamp": ["gte", "lte"],
        "reviewer_user": ["exact"],
    }

    permission_classes = [
        ActionIs("list")
        & (
            curriculum_permissions.IsCurrentUserInRecruitsForFilteredProject
            | curriculum_permissions.IsCurrentUserInReviewersForFilteredProject
            | core_permissions.IsCurrentUserInSpecificFilter("reviewer_user")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter(
                    "reviewer_user"
                ),
            )
        )
        | ActionIs("retrieve")
        & (
            core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=_get_teams_from_recruit_project_review,
            )
        )
    ]


class RecruitProjectReviewViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RecruitProjectReviewSerializer
    queryset = models.RecruitProjectReview.objects.order_by("-timestamp")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "timestamp": ["gte", "lte"],
        "status": ["exact"],
        "reviewer_user": ["exact"],
        "recruit_project": ["exact"],
        "recruit_project__recruit_users": ["exact"],
    }

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
                get_objects=core_permissions.get_teams_from_user_filter(
                    "recruit_project__recruit_users"
                ),
            )
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter(
                    "reviewer_user"
                ),
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
                permissions=Team.PERMISSION_VIEW, get_objects=_get_teams_from_repository
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
                get_objects=core_permissions.get_teams_from_user_filter(
                    "attendee_user"
                ),
            )
        )
    ]


class ManagementActionsViewSet(viewsets.ViewSet):

    serializer_class = core_serializers.NoArgs

    def list(self, request):
        return Response([])

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.TeamReviewByOtherSerialiser,
        permission_classes=[DenyAll],  # TODO
    )
    def team_review_by_other(self, request, pk=None):
        """grab users from another group and randomise them as reviewers for this group"""
        serialiser = get_serialiser(data=request.post)
        if serialiser.is_valid:
            serialiser.reviewer_group

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.TeamReviewByUserSerialiser,
        permission_classes=[DenyAll],  # TODO
    )
    def assign_user_as_reviewer(self, request, pk=None):
        todo

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=core_serializers.NoArgs,
        permission_classes=[permissions.IsAdminUser],
    )
    def auto_assign_reviewers(self, request, pk=None):
        """automatically assign qualified reviewers to cards"""
        if request.method == "GET":
            return Response({"status": "OK"})
        else:
            from long_running_request_actors import auto_assign_reviewers as actor

            response = actor.send()
            return Response({"status": "OK", "data": response.asdict()})

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.BulkSetDueDatesHumanFriendly,
        permission_classes=[permissions.IsAdminUser],
    )
    def bulk_set_due_dates(self, request, pk=None):
        """This is a human-friendly(ish) way to set due dates in bulk. It has more human readable input that the other mechanisms for setting due dates in bulk"""
        # TODO: REFACTOR. If the management helper is used ourtside the management dir then it should be moved
        from curriculum_tracking.management.helpers import get_user_cards

        if request.method == "GET":
            return Response({"status": "OK"})

        serializer = serializers.BulkSetDueDatesHumanFriendly(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            flavour_names = data.get("flavour_names", [])
            due_time = data.get("due_time")
            content_item_title = data.get("content_item_title")
            team_name = data.get("team_name")
            email = data.get("email")

            if team_name and email:
                return Response(
                    {"email": ["You can't specify an email and a team, pick one"]}
                )
            try:
                content_item = models.ContentItem.objects.get(title=content_item_title)
            except models.ContentItem.DoesNotExist:
                return Response(
                    {
                        "content_item_title": [
                            "Content item matching title does not exist"
                        ]
                    }
                )

            users = User.get_users_from_identifier(email or team_name)
            cards = get_user_cards(users, content_item)
            for card in cards:
                if card.flavours_match(flavour_names):
                    card.set_due_time(due_time)

            return Response(
                [serializers.CardSummarySerializer(card).data for card in cards]
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=serializers.RegisterNewLearnerSerializer,
        permission_classes=[permissions.IsAdminUser],
    )
    def register_new_learner(self, request, pk=None):
        serializer = serializers.RegisterNewLearnerSerializer(data=request.data)
        if serializer.is_valid():

            email = serializer.data["email"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            github_name = serializer.data["github_name"]
            stream_name = serializer.data["stream_name"]
            team_name = serializer.data["team_name"]

            try:
                stream = Stream.objects.get(name=stream_name)
            except Stream.DoesNotExist:
                return Response(
                    {
                        "stream_name": f'Stream matching name "{stream_name}" does not exist'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if stream.stream_curriculums.count() == 0:
                return Response(
                    {
                        "stream_name": f'Stream matching name "{stream_name}" does not have any courses. Please make sure it is set up correctly'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.get_or_create(
                email=email, defaults={"first_name": first_name, "last_name": last_name}
            )[0]
            user.active = True
            user.save()

            profile = SocialProfile.objects.get_or_create(user=user)[0]
            profile.github_name = github_name
            profile.save()

            team = Team.objects.get_or_create(name=team_name)[0]
            team.user_set.add(user)

            curriculum_ids = [
                o.curriculum_id for o in stream.stream_curriculums.order_by("order")
            ]
            existing = models.CourseRegistration.objects.filter(user=user)
            for o in existing:
                if o.curriculum_id not in curriculum_ids:
                    o.delete()
            for i, curriculum_id in enumerate(curriculum_ids):
                o, created = models.CourseRegistration.objects.get_or_create(
                    user=user, curriculum_id=curriculum_id, defaults={"order": i}
                )
                if not created:
                    o.order = i
                    o.save()

            return Response({"user_id": user.id})  # TODO: use a serializer rather

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BurnDownSnapShotViewset(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAdminUser
        | ActionIs("list")
        & (
            IsCurrentUserInSpecificFilter("user__id")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter("user__id"),
            )
        )
    ]

    serializer_class = serializers.BurnDownSnapShotSerializer
    queryset = models.BurndownSnapshot.objects.order_by("-timestamp")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user__id", "timestamp"]


class ReviewTrustsViewSet(viewsets.ModelViewSet):

    permission_classes = [
        permissions.IsAdminUser
        | ActionIs("list")
        & (
            core_permissions.IsCurrentUserInSpecificFilter("user")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter("user"),
            )
        )
    ]

    queryset = models.ReviewTrust.objects.order_by("user").all()
    serializer_class = serializers.ReviewTrustSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]


class ContentItemAgileWeightViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]

    queryset = models.ContentItemAgileWeight.objects.order_by("content_item").all()
    serializer_class = serializers.ContentItemAgileWeightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["content_item", "weight"]


class CourseRegistrationViewset(viewsets.ModelViewSet):
    queryset = models.CourseRegistration.objects.all().order_by("user")
    filterset_fields = ["user", "curriculum"]
    serializer_class = serializers.CourseRegistrationSerialiser
    filter_backends = [DjangoFilterBackend]
    permission_classes = [
        permissions.IsAdminUser
        | ActionIs("list")
        & (
            core_permissions.IsCurrentUserInSpecificFilter("user")
            | core_permissions.HasObjectPermission(
                permissions=Team.PERMISSION_VIEW,
                get_objects=core_permissions.get_teams_from_user_filter("user"),
            )
        )
    ]


class _ProjectReviewQueueViewSetBase(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectReviewQueueSerializer
    filter_backends = [DjangoFilterBackend]

    permission_classes = [IsReadOnly]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        queryset = super().get_queryset(*args, **kwargs)

        return self.filter_by_view_permission(queryset, user)

    def filter_by_view_permission(self, queryset, user):
        if user.is_superuser:
            return queryset

        filter = Q(recruit_users__in=[user]) | Q(reviewer_users__in=[user])

        for PERMISSION in Team.PERMISSION_VIEW:

            teams = get_objects_for_user(user, PERMISSION, Team)
            for team in teams:
                team_users = team.user_set.all()
                filter = (
                    filter
                    | Q(recruit_users__in=team_users)
                    | Q(reviewer_users__in=team_users)
                )

        queryset = queryset.filter(filter)
        return queryset


class CompetenceReviewQueueViewSet(_ProjectReviewQueueViewSetBase):

    filterset_fields = [
        "recruit_users",
        "reviewer_users",
        "code_review_competent_since_last_review_request",
        "code_review_excellent_since_last_review_request",
        "code_review_red_flag_since_last_review_request",
        "code_review_ny_competent_since_last_review_request",
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = (
            models.RecruitProject.objects.filter(
                agile_card__status=models.AgileCard.IN_REVIEW
            )
            .exclude(
                content_item__tags__name="technical-assessment"
            )  # TODO: remove this once LX have sorted out the problem with assessment cards never ever being closed :/ Two bugs do make a right sometimes
            .filter(recruit_users__active__in=[True])
            .order_by("review_request_time")
        )
        user = self.request.user
        return self.filter_by_view_permission(queryset, user)


class PullRequestReviewQueueViewSet(_ProjectReviewQueueViewSetBase):
    queryset = (
        models.RecruitProject.objects.filter(recruit_users__active__in=[True])
        .filter(
            repository__pull_requests__in=git_models.PullRequest.objects.filter(
                state="open"
            )
        )
        .exclude(
            agile_card__status=models.AgileCard.COMPLETE
        )
        .annotate(
            pr_time=Max("repository__pull_requests__updated_at"),
        )
        .order_by("pr_time")
    )
    filterset_fields = [
        "recruit_users",
        "reviewer_users",
    ]


class CurriculumContentRequirementViewset(viewsets.ModelViewSet):
    queryset = models.CurriculumContentRequirement.objects.all().order_by(
        "curriculum_id"
    )
    filterset_fields = ["curriculum", "content_item"]
    serializer_class = serializers.CurriculumContentRequirementSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [permissions.IsAdminUser]


# from curriculum_tracking.models import *
# from django.utils import timezone
# from django.db.models import  F
# from django.contrib.postgres.aggregates import *
# # class UserReviewPerformance(viewsets.ModelViewSet):
#     RecruitProjectReview.objects.filter(reviewer_user__email="vuyisanani.meteni@umuzi.org").filter(timestamp__gte = timezone.now() - timezone.timedelta(days=7)).annotate(flavour_names=StringAgg('recruit_project__flavours__name',delimiter=",", ordering= 'recruit_project__flavours__name')).values('id','flavour_names','recruit_project__content_item_id')
