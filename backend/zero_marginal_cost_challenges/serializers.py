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
