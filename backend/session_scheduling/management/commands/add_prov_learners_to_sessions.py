"""
Get the learners who are in prov and bridging groups, who have assessment cards that dont have competent reviews yet.

Find fundamental skill assistance sessions with empty seats

Add the prov learners into the existing sessions
"""

from django.core.management.base import BaseCommand
from session_scheduling.models import Session, SessionType
from session_scheduling.session_types import SESSION_FUNDAMENTAL_SKILL_ASSISTANCE
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from curriculum_tracking.models import AgileCard
from selection_bootcamps.models import ProvisionalGroup
from ..helpers import card_name_skill_name_mapping, get_skill_name_from_pod_column_name
import random

User = get_user_model()
MAX_SESSION_SIZE = 3


def get_prov_users():
    prov_groups = ProvisionalGroup.objects.filter(active=True).prefetch_related("team")
    users = []
    for prov_group in prov_groups:
        users.extend(list(prov_group.team.active_users))
    random.shuffle(users)
    return users


def get_user_assessment_cards(user):
    cards = (
        AgileCard.objects.filter(content_item__title__startswith="Assessment:")
        .filter(assignees=user)
        .filter(~Q(status=AgileCard.COMPLETE))
        .filter(~Q(status=AgileCard.BLOCKED))
        .filter(recruit_project__code_review_competent_since_last_review_request=0)
        .prefetch_related("content_item")
    )
    return (
        card
        for card in cards
        if card.content_item.title in card_name_skill_name_mapping
    )


def get_session_user_can_join(card):
    """
    find sessions with the type SESSION_FUNDAMENTAL_SKILL_ASSISTANCE
    the flavours need to match the card
    and the extra title text needs to match the card
    and the number of people in the session must be less than MAX_SESSION_SIZE
    """
    title = card.content_item.title
    nice_skill_name = get_skill_name_from_pod_column_name(
        card_name_skill_name_mapping[title]
    )
    flavours = card.flavour_names

    session_type = SessionType.objects.get(name=SESSION_FUNDAMENTAL_SKILL_ASSISTANCE)

    sessions = (
        Session.objects.filter(session_type=session_type)
        .filter(is_cancelled=False)
        .filter(is_complete=False)
        .annotate(session_size=Count("attendees"))
        .filter(session_size__lt=MAX_SESSION_SIZE)
        .filter(extra_title_text=nice_skill_name)
        .order_by("session_size")
    )

    for s in sessions:
        if s.flavours_match(flavours):
            return s


# def create_new_sessions_for_users_without_sessions():


def add_prov_learners_to_sessions():
    users = get_prov_users()
    users_added_to_sessions = []

    total = len(users)
    for i, user in enumerate(users):
        print(f"{i+1}/{total}: {user}")
        cards = get_user_assessment_cards(user)
        for card in cards:
            session = get_session_user_can_join(card)
            if session:
                session.attendees.add(user)
                users_added_to_sessions.append(user)
                break
    # now we might have some users who did not get added to any sessions at all
    users_not_added = [user for user in users if user not in users_added_to_sessions]

    print("=====================")
    print(f"USERS NOT ADDED")
    print(users_not_added)
    print("=====================")

    # create_new_sessions_for_users_without_sessions(users_not_added)


class Command(BaseCommand):
    def handle(self, *args, **options):
        add_prov_learners_to_sessions()
        print("Done")
