from rest_framework import serializers
from . import models
from curriculum_tracking.models import ContentItem
from rest_framework.authtoken.models import Token


class ChallengeRegistrationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChallengeRegistration
        fields = [
            "id",
            "user",
            "curriculum",
            "registration_date",
        ]


class ChallengeRegistrationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChallengeRegistration
        fields = [
            "id",
            "user",
            "curriculum",
            "registration_date",
            "blurb",
            "steps",
            "name",
        ]

    blurb = serializers.SerializerMethodField("get_blurb")
    name = serializers.SerializerMethodField("get_name")
    steps = serializers.SerializerMethodField("get_steps")

    def get_name(self, instance):
        return instance.curriculum.name

    def get_blurb(self, instance):
        return instance.curriculum.blurb

    def get_steps(self, instance):
        steps = instance.get_steps()

        return [
            {
                "title": step.content_item.title,
                "blurb": step.content_item.blurb,
                "status": step.status,
            }
            for step in steps
        ]


class StepIndexSerializer(serializers.Serializer):
    """Used in actions that target a specific step associated with a challenge. Eg start step 3"""

    class Meta:
        fields = ["index"]

    index = serializers.IntegerField()


class StepDetailsSerializer(serializers.Serializer):
    class Meta:
        fields = [
            "content_type",
            "raw_url",
            "project_submission_type",
            "link_name",
            "link_example",
            "link_message",
            "link_submission",
            "reviews",
            "title",
            "status",
            "blurb",
        ]

    content_type = serializers.SerializerMethodField("get_content_type")
    raw_url = serializers.SerializerMethodField("get_raw_url")
    project_submission_type = serializers.SerializerMethodField(
        "get_project_submission_type"
    )
    link_name = serializers.SerializerMethodField("get_link_name")
    link_example = serializers.SerializerMethodField("get_link_example")
    link_message = serializers.SerializerMethodField("get_link_message")
    link_submission = serializers.SerializerMethodField("get_link_submission")
    reviews = serializers.SerializerMethodField("get_reviews")
    title = serializers.SerializerMethodField("get_title")
    status = serializers.SerializerMethodField("get_status")
    blurb = serializers.SerializerMethodField("get_blurb")

    def get_content_type(self, instance):
        return instance.content_item.content_type

    def get_raw_url(self, instance):
        return instance.content_item.raw_url

    def get_project_submission_type(self, instance):
        return instance.content_item.project_submission_type

    def get_link_name(self, instance):
        return instance.content_item.link_name

    def get_link_example(self, instance):
        return instance.content_item.link_example

    def get_link_message(self, instance):
        return instance.content_item.link_message

    def get_link_submission(self, instance):
        progress = instance.progress
        if progress == None:
            return
        if instance.content_item.content_type == ContentItem.PROJECT:
            return instance.progress.link_submission

    def get_reviews(self, instance):
        if instance.content_item.content_type != ContentItem.PROJECT:
            return []

        progress = instance.progress
        if progress == None:
            return []

        return [
            {
                "timestamp": o.timestamp,
                "status": o.status,
                "comments": o.comments,
            }
            for o in progress.project_reviews.order_by("-timestamp")
        ]

    def get_title(self, instance):
        return instance.content_item.title

    def get_status(self, instance):
        return instance.status

    def get_blurb(self, instance):
        return instance.content_item.blurb


class SubmitLinkSerializer(serializers.Serializer):
    class Meta:
        fields = ["index", "link_submission"]

    index = serializers.IntegerField()
    link_submission = serializers.URLField()


class WhoAmISerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = [
            "email",
            # "token",
            "user_id",
            # "active",
            "first_name",
            # "last_name",
            # "preferred_name",
            # "is_staff",
            # "is_superuser",
            # "permissions",
            # "teams",
        ]

    email = serializers.SerializerMethodField("get_email")
    first_name = serializers.SerializerMethodField("get_first_name")

    # preferred_name = serializers.SerializerMethodField("get_preferred_name")
    # token = serializers.SerializerMethodField("get_token")
    # active = serializers.SerializerMethodField("get_active")
    # last_name = serializers.SerializerMethodField("get_last_name")
    # is_staff = serializers.SerializerMethodField("get_is_staff")
    # is_superuser = serializers.SerializerMethodField("get_is_superuser")
    # permissions = serializers.SerializerMethodField("get_permissions")
    # teams = serializers.SerializerMethodField("get_teams")
    # is_student = serializers.SerializerMethodField("get_is_student")

    def get_email(self, instance):
        return instance.user.email

    def get_first_name(self, instance):
        return instance.user.first_name
