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
        user = instance.user

        content_items = [
            o.content_item
            for o in instance.curriculum.content_requirements.prefetch_related(
                "content_item"
            )
        ]

        def get_progress(item):
            if item.content_type == ContentItem.PROJECT:
                return (
                    RecruitProject.objects.filter(recruit_users=user)
                    .filter(content_item=item)
                    .first()
                )
            if item.content_type == ContentItem.TOPIC:
                return (
                    TopicProgress.objects.filter(user=user)
                    .filter(content_item=item)
                    .first()
                )

        STATUS_DONE = "DONE"
        STATUS_BLOCKED = "BLOCKED"
        STATUS_READY = "READY"

        progress = [get_progress(item) for item in content_items]

        latest_complete = -1
        for i, p in enumerate(progress):
            if p == None:
                break
            if p.complete_time:
                latest_complete = i
            else:
                break

        def _get_status(i, latest_complete):
            if i <= latest_complete:
                return STATUS_DONE
            if i == latest_complete + 1:
                return STATUS_READY
            return STATUS_BLOCKED

        return [
            {
                "title": item.title,
                "blurb": item.blurb,
                "status": _get_status(i, latest_complete),
            }
            for (i, item) in enumerate(content_items)
        ]
