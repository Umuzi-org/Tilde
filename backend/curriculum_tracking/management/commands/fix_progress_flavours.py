"""when updating content from the syllabus, flavour names can change. This script goes over all content items and then gets topic/project/workshop progress instances that match each content item and then updates their flavours accordingly"""

from curriculum_tracking.models import (
    ContentItem,
    WorkshopAttendance,
    TopicProgress,
    RecruitProject,
)

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        content_items = ContentItem.objects.all()
        total = content_items.count()
        for i, content_item in enumerate(content_items):
            print(f"{i+1}/{total} {content_item}")
            flavour_strings = content_item.flavour_names
            for Model in [WorkshopAttendance, TopicProgress, RecruitProject]:
                progress = Model.objects.filter(content_item=content_item)
                for o in progress:
                    o.set_flavours(flavour_strings)
