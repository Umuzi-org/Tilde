from django.core.management.base import BaseCommand
from automarker.management.command_utils import get_config_from_file
from curriculum_tracking.models import ContentItem
from automarker.models import ContentItemAutoMarkerConfig
from pathlib import Path


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("config_repo_path", type=str)

    def handle(self, *args, **options):
        breakpoint()
        ingest_automarker_config(Path(options.get("config_repo_path")))


def ingest_automarker_config(config_file_path):
    config = get_config_from_file(config_file_path / "config.yaml")

    seen_instances_in_file = []
    seen_config_ids = []

    for item in config:
        content_item = ContentItem.objects.get(pk=item["contentItemId"])
        flavour_names = item["flavours"]
        mode = item["mode"]

        fingerprint = f"{content_item.id} {sorted(flavour_names)}"
        assert (
            fingerprint not in seen_instances_in_file
        ), "duplicate config in config.yaml file. {fingerprint}"

        seen_instances_in_file.append(fingerprint)

        item_configs = ContentItemAutoMarkerConfig.objects.filter(
            content_item=content_item
        )
        matching_configs = [o for o in item_configs if o.flavours_match(flavour_names)]

        if len(matching_configs) == 0:
            # create one
            o = ContentItemAutoMarkerConfig.objects.create(
                content_item=content_item, mode=mode
            )
            o.set_flavours(flavour_names)
        else:
            assert (
                len(matching_configs) == 1
            ), f"Too many config instances in the db, {content_item} {flavour_names}"
            o = matching_configs[0]
            o.mode = mode
            o.save()
        seen_config_ids.append(o.id)

    # remove what shouldn't be there

    for o in list(ContentItemAutoMarkerConfig.objects.all()):
        if o.id not in seen_config_ids:
            o.delete()
