from django.core.management.base import BaseCommand
from core.models import User
from curriculum_tracking.models import CourseRegistration, Curriculum


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("curriculum_name", type=str)
        parser.add_argument("order", type=int, nargs="?")
        # parser.add_argument("curriculum_name", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(email=options["email"])
        curriculum = Curriculum.objects.get(name=options["curriculum_name"])

        order = options.get("order")
        defaults = {}
        if order:
            defaults = {"order": order}

        reg, created = CourseRegistration.objects.get_or_create(
            user=user, curriculum=curriculum, defaults=defaults
        )

        if created:
            print("created")
        else:
            if order:
                reg.order = order
                reg.save()
                print("updated order")