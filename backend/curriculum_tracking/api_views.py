from rest_framework import mixins
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters, status

User = get_user_model()

from . import models
from . import serializers
from view_mixins import AuthMixin
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from core import permissions as core_permissions
from curriculum_tracking import permissions as curriculum_permissions

from rest_framework.decorators import action
from django.http import Http404, HttpResponseForbidden
from django.utils import timezone

from git_real import serializers as git_serializers
from git_real import models as git_models

from django.db.models import Q


class ProjectCardSummaryViewset(AuthMixin, viewsets.ModelViewSet):
    # TODO: make this view only
    permission_classes = [
        permissions.IsAdminUser
        | core_permissions.IsStaffUser
        | core_permissions.IsCurrentUserInSpecificFilter("assignees")
    ]

    serializer_class = serializers.ProjectCardSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["assignees"]

    queryset = (
        models.AgileCard.objects.order_by("order")
        .filter(content_item__content_type=models.ContentItem.PROJECT)
        # .filter(Q(is_hard_milestone=True) | Q(is_soft_milestone=True))
        .prefetch_related("content_item")
        .prefetch_related("recruit_project")
    )


class AgileCardViewset(AuthMixin, viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAdminUser
        | core_permissions.IsStaffUser
        | core_permissions.IsCurrentUserInSpecificFilter("assignees")
        | core_permissions.IsCurrentUserInSpecificFilter("reviewers")
        # curriculum_permissions.ProjectOrReviewIsMine
        | curriculum_permissions.CardBelongsToRequestingUser
    ]

    serializer_class = serializers.AgileCardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["assignees", "reviewers", "status"]

    def get_queryset(self):
        return models.AgileCard.objects.order_by("order").prefetch_related(
            "recruit_project"
        )

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.SetDueTimeSerializer,
        permission_classes=[
            permissions.IsAdminUser
            | core_permissions.IsStaffUser
            | (
                curriculum_permissions.IsCardAssignee
                & curriculum_permissions.CardDueTimeIsNotSet
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
            | permissions.IsAdminUser
            | core_permissions.IsStaffUser
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
                    timestamp=timezone.datetime.now(),
                    comments=serializer.data["comments"],
                    recruit_project=card.recruit_project,
                    reviewer_user=request.user,
                )
            elif card.content_item.content_type == models.ContentItem.TOPIC:
                if card.topic_progress == None:
                    raise Http404

                review = models.TopicReview.objects.create(
                    status=serializer.data["status"],
                    timestamp=timezone.datetime.now(),
                    comments=serializer.data["comments"],
                    topic_progress=card.topic_progress,
                    reviewer_user=request.user,
                )

            review.save()
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
            | permissions.IsAdminUser
            | core_permissions.IsStaffUser
        ],
    )
    def request_review(self, request, pk=None):
        card: models.AgileCard = self.get_object()
        if card.recruit_project == None:
            raise Http404
        card.recruit_project.request_review(force_timestamp=timezone.now())
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
            | permissions.IsAdminUser
            | core_permissions.IsStaffUser
        ],
    )
    def cancel_review_request(self, request, pk=None):
        card = self.get_object()
        if card.status != models.AgileCard.IN_REVIEW:
            raise Http404()
        card.recruit_project.cancel_request_review()
        card.status = models.AgileCard.IN_PROGRESS
        card.save()
        return Response(serializers.AgileCardSerializer(card).data)

    def get_card_or_error(self, status_or_404, type_or_404):
        card = self.get_object()
        if status_or_404 and card.status != status_or_404:
            raise Http404()
        if card.content_type != dict(models.ContentItem.CONTENT_TYPES)[type_or_404]:
            raise Http404()

        return card

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NoArgs,
        permission_classes=[
            curriculum_permissions.IsCardAssignee
            | permissions.IsAdminUser
            | core_permissions.IsStaffUser
        ],
    )
    def start_project(self, request, pk=None):
        card = self.get_card_or_error(
            # status_or_404=models.AgileCard.READY,
            status_or_404=None,
            type_or_404=models.ContentItem.PROJECT,
        )
        user = request.user
        if user.is_staff or user.is_superuser:
            if card.status not in [models.AgileCard.READY, models.AgileCard.BLOCKED]:
                raise Http404()
        else:
            assert user in card.assignees.all()
            if not card.can_start():
                return Response(serializers.AgileCardSerializer(card).data)

        card.start_project()
        return Response(serializers.AgileCardSerializer(card).data)

    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.ProjectSubmitLink,
        permission_classes=[
            curriculum_permissions.IsCardAssignee
            | permissions.IsAdminUser
            | core_permissions.IsStaffUser
        ],
    )
    def set_project_link(self, request, pk=None):
        card = self.get_card_or_error(
            status_or_404=None, type_or_404=models.ContentItem.PROJECT,
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
            curriculum_permissions.IsCardAssignee
            | permissions.IsAdminUser
            | core_permissions.IsStaffUser
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
            | permissions.IsAdminUser
            | core_permissions.IsStaffUser
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
            | permissions.IsAdminUser
            | core_permissions.IsStaffUser
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
        permission_classes=[permissions.IsAdminUser | core_permissions.IsStaffUser],
    )
    def mark_workshop_attendance(self, request, pk=None):

        card = self.get_card_or_error(
            status_or_404=None, type_or_404=models.ContentItem.WORKSHOP
        )
        card.attended_workshop(timestamp=timezone.datetime.now())
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
            # curriculum_permissions.IsCardAssignee |
            permissions.IsAdminUser
            | core_permissions.IsStaffUser
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


class RecruitProjectViewset(AuthMixin, viewsets.ModelViewSet):

    serializer_class = serializers.RecruitProjectSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["recruit_users"]

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [
                curriculum_permissions.IsProjectAssignee
                | curriculum_permissions.IsProjectReviewer
                | permissions.IsAdminUser
                | core_permissions.IsStaffUser
            ]
        else:
            permission_classes = [
                permissions.IsAdminUser
                | core_permissions.IsStaffUser
                | core_permissions.IsCurrentUserInSpecificFilter("recruit_users")
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return models.RecruitProject.objects.order_by("pk").prefetch_related(
            "agile_card", "content_item"
        )


class TopicProgressViewset(AuthMixin, viewsets.ModelViewSet):
    serializer_class = serializers.TopicProgressSerializer
    queryset = models.TopicProgress.objects.order_by("pk")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user"]

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [
                curriculum_permissions.IsTopicProgressUser
                | permissions.IsAdminUser
                | core_permissions.IsStaffUser
            ]
        else:
            permission_classes = [
                permissions.IsAdminUser
                | core_permissions.IsStaffUser
                | core_permissions.IsCurrentUserInSpecificFilter("user")
            ]

        return [permission() for permission in permission_classes]


class TopicReviewViewset(AuthMixin, viewsets.ModelViewSet):
    serializer_class = serializers.TopicReviewSerializer
    queryset = models.TopicReview.objects.order_by("pk")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "status",
        "reviewer_user",
        "topic_progress"
        #  'recruit_users'  # TODO. Add
    ]

    def get_permissions(self):
        permission_classes = [
            permissions.IsAdminUser
            | core_permissions.IsStaffUser
            | core_permissions.IsCurrentUserInSpecificFilter("reviewer_user")
            | curriculum_permissions.IsCurrentUserInUsersForFilteredTopicProgress
            # | curriculum_permissions.IsCurrentUserInReviewersForFilteredTopicProgress
        ]
        return [permission() for permission in permission_classes]


class RecruitProjectReviewViewset(AuthMixin, viewsets.ModelViewSet):
    serializer_class = serializers.RecruitProjectReviewSerializer
    queryset = models.RecruitProjectReview.objects.order_by("pk")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "status",
        "reviewer_user",
        "recruit_project"
        #  'recruit_users'  # TODO. Add
    ]

    def get_permissions(self):

        # if self.action == 'retrieve':
        # else:
        permission_classes = [
            permissions.IsAdminUser
            | core_permissions.IsStaffUser
            | core_permissions.IsCurrentUserInSpecificFilter("recruit_users")
            | core_permissions.IsCurrentUserInSpecificFilter("reviewer_users")
            | curriculum_permissions.IsCurrentUserInRecruitsForFilteredProject
            | curriculum_permissions.IsCurrentUserInReviewersForFilteredProject
        ]
        return [permission() for permission in permission_classes]

    # def progress_report(self):
    #     RecruitProjectReview.objects.filter(timestamp__gte=before).values('reviewer_user','reviewer_user__email', 'reviewer_user__is_staff','recruit_project__content_item__title').annotate(dcount=Count('reviewer_user'))


class ContentItemViewset(AuthMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ContentItemSerializer
    queryset = models.ContentItem.objects.order_by("pk")


class ContentItemOrderViewset(AuthMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ContentItemOrderSerializer
    queryset = models.ContentItemOrder.objects.order_by("pk")


class RepositoryViewset(AuthMixin, viewsets.ModelViewSet):
    serializer_class = git_serializers.RepositorySerializer
    queryset = git_models.Repository.objects.all()

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [
                curriculum_permissions.IsRepoAttachedToProjectICanSee
                | permissions.IsAdminUser
                | core_permissions.IsStaffUser
            ]
        else:
            permission_classes = [
                permissions.IsAdminUser | core_permissions.IsStaffUser
            ]
        return [permission() for permission in permission_classes]


class CommitViewSet(AuthMixin, viewsets.ModelViewSet):
    serializer_class = git_serializers.CommitSerializer
    queryset = git_models.Commit.objects.order_by("-datetime")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["repository"]

    def get_permissions(self):
        permission_classes = [
            permissions.IsAdminUser
            | core_permissions.IsStaffUser
            | curriculum_permissions.IsFilteredByRepoAttachedToProjectICanSee
        ]
        return [permission() for permission in permission_classes]


class PullRequestViewSet(AuthMixin, viewsets.ModelViewSet):
    serializer_class = git_serializers.PullRequestSerializer
    queryset = git_models.PullRequest.objects.order_by("-created_at")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["repository"]

    def get_permissions(self):
        permission_classes = [
            permissions.IsAdminUser
            | core_permissions.IsStaffUser
            | curriculum_permissions.IsFilteredByRepoAttachedToProjectICanSee
        ]
        return [permission() for permission in permission_classes]


class PullRequestReviewViewSet(AuthMixin, viewsets.ModelViewSet):
    serializer_class = git_serializers.PullRequestReviewSerializer
    queryset = git_models.PullRequestReview.objects.order_by("-submitted_at")
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["pull_request"]


class ManagmentActionsViewSet(viewsets.ViewSet):
    serializer_class = serializers.NoArgs

    def list(self, request):
        return Response([])

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.GroupSelfReviewSerialiser,
        permission_classes=[
            core_permissions.IsReadOnly | curriculum_permissions.IsGroupManager("group")
        ],
    )
    def group_self_review_random(self, request, pk=None):
        """randomise group members and assign them as reviewers to each others cards for a specific project"""
        if request.method == "GET":
            return Response()
        todo

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.GroupReviewByOtherSerialiser,
        permission_classes=[
            curriculum_permissions.IsGroupManager("group")
            & curriculum_permissions.IsGroupManager("reviewer_group")
        ],
    )
    def group_review_by_other(self, request, pk=None):
        """grab users from another group and randomise them as reviewers for this group"""
        todo

    @action(
        detail=False,
        methods=["post", "get"],
        serializer_class=serializers.GroupReviewByUserSerialiser,
        permission_classes=[
            curriculum_permissions.IsGroupManager("group")
            & curriculum_permissions.IsUserManager("reviewer_user")
        ],
    )
    def assign_user_as_reviewer(self, request, pk=None):
        todo

    # TODO: bulk set due dates


class WorkshopAttendanceViewset(AuthMixin, viewsets.ModelViewSet):
    
    serializer_class = serializers.WorkshopAttendanceSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["attendee_user"]

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [
                curriculum_permissions.IsProjectAssignee
                | permissions.IsAdminUser
                | core_permissions.IsStaffUser
            ]
        else:
            permission_classes = [
                permissions.IsAdminUser
                | core_permissions.IsStaffUser
                | core_permissions.IsCurrentUserInSpecificFilter("attendee_user")
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return models.WorkshopAttendance.objects.order_by("pk").prefetch_related(
            "agile_card", "content_item", "flavours",
        )

