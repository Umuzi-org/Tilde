from django.db import models
from curriculum_tracking.models import FlavourMixin, ContentItemProxyMixin, ContentItem
from taggit.managers import TaggableManager


class ContentItemAutoMarkerConfig(models.Model, FlavourMixin, ContentItemProxyMixin):
    MODE_DEBUG = "debug"
    MODE_PROD = "prod"
    MODE_DEACTIVATED = "deactivated"

    MODES = [
        (MODE_DEBUG, MODE_DEBUG),
        (MODE_PROD, MODE_PROD),
        (MODE_DEACTIVATED, MODE_DEACTIVATED),
    ]

    content_item = models.ForeignKey(
        ContentItem, on_delete=models.PROTECT, related_name="automarker_configs"
    )
    flavours = TaggableManager(blank=True)
    mode = models.CharField(null=False, blank=False, choices=MODES, max_length=11)
