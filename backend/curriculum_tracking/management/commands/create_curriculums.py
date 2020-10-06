from django.core.management.base import BaseCommand
from core.models import Curriculum


class Command(BaseCommand):
    def handle(self, *args, **options):

        for s in [
            "strat",
            "data sci",
            "web dev",
            "data eng",
            "copy",
            "ui",
            "java",
            "Multimedia",
            "ui and adv",
            "adv",
            "copy and adv",
            "ios mobile",
            "hybrid mobile short",
            "andriod kotlin",
            "data sci prebootcamp",
            "web dev pre boot",
            "java bridging course",
            "web dev bridging",
            "data sci boot",
            "web dev boot",
            "web dev no nqf",
            "react specialisation",
            "django for web devs",
            "django for data sci",
        ]:
            Curriculum.objects.get_or_create(short_name=s, name=s)

