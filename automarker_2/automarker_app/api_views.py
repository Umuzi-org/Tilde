from rest_framework import permissions, viewsets
from rest_framework.response import Response
from django.http import Http404

from . import serializers

from .lib.marker import mark_project, get_final_review
from automarker_app.lib import constants


class MarkProjectViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.MarkProjectInputSerializer

    def create(self, request):
        serializer = serializers.MarkProjectInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        steps = mark_project(
            content_item_id=serializer.validated_data["content_item_id"],
            flavours=serializer.validated_data["flavours"],
            url=serializer.validated_data["url"],
        )

        status, comments = get_final_review(steps)

        response_serializer = serializers.MarkProjectOutputSerializer(
            data={
                "status": status,
                "comments": comments,
            }
        )
        breakpoint()
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.data)

    def retrieve(self, request, pk=None):
        raise Http404

    def update(self, request, pk=None):
        raise Http404

    def partial_update(self, request, pk=None):
        raise Http404

    def destroy(self, request, pk=None):
        raise Http404

    def list(self, request):
        return Response({})
