from rest_framework import serializers
from . import models
from curriculum_tracking.models import TopicProgress, RecruitProject, ContentItem


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
            "url",
            "project_submission_type",
            "link_name",
            "link_example",
            "link_message",
            "link_submission",
            "reviews",
        ]

    content_type = serializers.SerializerMethodField("get_content_type")
    url = serializers.SerializerMethodField("get_url")
    project_submission_type = serializers.SerializerMethodField(
        "get_project_submission_type"
    )
    link_name = serializers.SerializerMethodField("get_link_name")
    link_example = serializers.SerializerMethodField("get_link_example")
    link_message = serializers.SerializerMethodField("get_link_message")
    link_submission = serializers.SerializerMethodField("get_link_submission")
    reviews = serializers.SerializerMethodField("get_reviews")

    def get_content_type(self, instance):
        return instance.content_item.content_type

    def get_url(self, instance):
        return instance.content_item.url

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
            for o in progress.project_reviews.order_by("timestamp")
        ]
