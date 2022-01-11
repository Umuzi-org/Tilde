# python manage.py set_config_value "curriculum_tracking/serializers/TeamStatsSerializer" "EXCLUDE_TAGS_FROM_REVIEW_STATS" "ncit" 1 s

from django.core.management.base import BaseCommand

from config import models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("namespace", type=str)
        parser.add_argument("value_name", type=str)
        parser.add_argument("value_value", type=str)
        parser.add_argument("value_repeated", type=int)
        parser.add_argument("value_datatype", type=str)

    def handle(self, *args, **options):
        namespace, _ = models.NameSpace.objects.get_or_create(
            name=options["namespace"], defaults={"description": ""}
        )
        defaults = {
            "value": options["value_value"],
            "repeated": bool(options["value_repeated"]),
            "datatype": options["value_datatype"],
        }

        models.Value.get_or_create_or_update(
            namespace=namespace,
            name=options["value_name"],
            defaults=defaults,
            overrides=defaults,
        )
