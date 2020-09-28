"""
This is for getting a look at the cards generated for a course

delete all progress beloning to a user
delete all course registrations for user
add single course registration
generate cards
"""
from django.core.management.base import BaseCommand
from core.models import Curriculum, User
from curriculum_tracking.models import AgileCard, CourseRegistration
from django.db.models import Q
from curriculum_tracking.card_generation_helpers import (
    generate_all_content_cards_for_user,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email", type=str)
        parser.add_argument("curriculum", type=str)

    def handle(self, *args, **options):
        user = User.objects.get(email=options["email"])
        AgileCard.objects.filter(assignees__in=[user]).delete()
        CourseRegistration.objects.filter(user=user).delete()

        name = options["curriculum"]
        curriculum = Curriculum.objects.get(Q(short_name=name) | Q(name=name))

        CourseRegistration.objects.create(user=user, curriculum=curriculum)

        generate_all_content_cards_for_user(user)

