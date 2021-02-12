from . import models
from rest_framework import serializers
from django.db.models import Q
from core import models as core_models


class RecruitProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProject
        fields = [
            "id",
            "content_item",
            "due_time",
            "complete_time",
            "repository",
            "project_reviews",
            "title",
            "content_url",
            "story_points",
            "tag_names",
            "recruit_users",
            "recruit_user_names",
            "reviewer_users",
            "reviewer_user_names",
            "agile_card",
            "agile_card_status",
            "submission_type_nice",
            "link_submission",
            # "deadline_status",
            # "latest_project_review_status",
            # "latest_project_review_timestamp",
            # "latest_project_review_comments",
            # "latest_project_reviewer_email",
        ]


class TopicProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TopicProgress
        fields = [
            "id",
            "user",
            "content_item",
            "due_time",
            "start_time",
            "complete_time",
            "review_request_time",
            "topic_reviews",
            "topic_needs_review",
            "flavours",
        ]

    flavours = serializers.CharField(help_text="comma seperated list of flavours")


class RecruitProjectReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProjectReview
        fields = [
            "id",
            "status",
            "timestamp",
            "comments",
            "recruit_project",
            "reviewer_user",
            "reviewer_user_email",
            # the below fields are not used when navigting a user's board.
            # there should probably be 2 seperate serialisers for the different displays
            "title",
            "reviewed_user_emails",
            "reviewed_user_ids",
            "trusted",
            "validated",
            "agile_card",
        ]

    agile_card = serializers.SerializerMethodField("get_agile_card")
    title = serializers.SerializerMethodField("get_title")
    reviewed_user_emails = serializers.SerializerMethodField("get_reviewed_user_emails")
    reviewed_user_ids = serializers.SerializerMethodField("get_reviewed_user_ids")

    def get_agile_card(self, instance):
        try:
            return instance.recruit_project.agile_card.id
        except models.AgileCard.DoesNotExist:
            return

    def get_title(self, instance):
        return instance.recruit_project.content_item.title

    def get_reviewed_user_emails(self, instance):
        return [o.email for o in instance.recruit_project.recruit_users.all()]

    def get_reviewed_user_ids(self, instance):
        return [o.id for o in instance.recruit_project.recruit_users.all()]


class TopicReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TopicReview
        fields = [
            "id",
            "status",
            "timestamp",
            "comments",
            "topic_progress",
            "reviewer_user",
            "reviewer_user_email",
        ]


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentItem
        fields = [
            "id",
            "content_type",
            "content_type_nice",
            "title",
            "slug",
            "url",
            "story_points",
            "tag_names",
            "post_ordered_content",
            "pre_ordered_content",
            "flavour_names",
            "topic_needs_review",
            "project_submission_type_nice",
            "continue_from_repo",
            "template_repo",
        ]


class ContentItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentItemOrder
        fields = ["id", "pre", "post", "hard_requirement", "pre_title", "post_title"]


class AgileCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgileCard
        fields = [
            "id",
            "content_item",
            "content_item_url",
            "status",
            "recruit_project",
            "assignees",
            "reviewers",
            "assignee_names",
            "reviewer_names",
            "is_hard_milestone",
            "is_soft_milestone",
            "title",
            "content_type",
            "content_type_nice",
            "story_points",
            "tag_names",
            "order",
            # "repository",
            "code_review_competent_since_last_review_request",
            "code_review_excellent_since_last_review_request",
            "code_review_red_flag_since_last_review_request",
            "code_review_ny_competent_since_last_review_request",
            "requires_cards",
            "required_by_cards",
            "flavour_names",
            "project_submission_type_nice",
            "project_link_submission",
            "topic_needs_review",
            "topic_progress",
            "due_time",
            "complete_time",
            "review_request_time",
            "start_time",
            "can_start",
            "can_force_start",
        ]


class cardsummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgileCard
        fields = [
            "id",
            "order",
            "content_item",
            "content_item_url",
            "title",
            "status",
            # "nice_status",
            # "project_due_time",
            "recruit_project",
            # "project_review_request_time",
            "due_time",
            "complete_time",
            "review_request_time",
            "start_time",
            "assignees",
            "assignee_names",
            "code_review_competent_since_last_review_request",
            "code_review_excellent_since_last_review_request",
            "code_review_red_flag_since_last_review_request",
            "code_review_ny_competent_since_last_review_request",
        ]


class NoArgs(serializers.Serializer):
    class Meta:
        fields = []


class NewReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProjectReview
        fields = [
            "status",
            "comments",
        ]


class WorkshopAttendanceTime(serializers.ModelSerializer):
    class Meta:
        model = models.WorkshopAttendance
        fields = ["timestamp"]


class AddReviewerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AgileCard
        fields = ["reviewers"]


class SetDueTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProject
        fields = ["due_time"]


class TeamField(serializers.RelatedField):
    queryset = core_models.Team.objects.filter(active=True).order_by("name")

    def to_representation(self, value):
        return value.id


class UserField(serializers.RelatedField):
    queryset = core_models.User.objects.filter(active=True).order_by("email")

    def to_representation(self, value):
        return value.id


class ProjectContentItemField(serializers.RelatedField):
    queryset = (
        models.ContentItem.objects.filter(content_type=models.ContentItem.PROJECT)
        .filter(~Q(project_submission_type=models.ContentItem.NO_SUBMIT))
        .order_by("title")
    )

    def to_representation(self, value):
        return value.id


class GroupSelfReviewSerialiser(serializers.Serializer):
    class Meta:
        fields = ["group", "content_item", "flavours"]

    content_item = ProjectContentItemField()
    flavours = serializers.CharField(help_text="comma seperated list of flavours")
    group = TeamField()


class TeamReviewByOtherSerialiser(serializers.Serializer):
    class Meta:
        fields = ["group", "content_item", "reviewer_group", "flavours"]

    content_item = ProjectContentItemField()
    flavours = serializers.CharField(help_text="comma seperated list of flavours")
    group = TeamField()
    reviewer_group = TeamField()


class TeamReviewByUserSerialiser(serializers.Serializer):
    class Meta:
        fields = [
            "group",
            "content_item",
            "reviewer_user",
            "flavours",
            "assign_to_cards",
        ]

    assign_to_cards = serializers.BooleanField(
        default=True,
        help_text="if this is false then the user is only assigned to the github repos. If it is True then the user is listed as a reviewer on the agile cards",
    )

    content_item = ProjectContentItemField()
    flavours = serializers.CharField(help_text="comma seperated list of flavours")
    group = TeamField()
    reviewer_user = serializers.EmailField()


class ProjectSubmitLink(serializers.ModelSerializer):
    class Meta:
        model = models.RecruitProject
        fields = ["link_submission"]

    # TODO: validators based on model validators (look inside save method)


class WorkshopAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkshopAttendance
        fields = [
            "id",
            "timestamp",
            "content_item",
            "attendee_user",
        ]
