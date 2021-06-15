from core.models import Team, User

from curriculum_tracking.models import AgileCard, RecruitProject
import logging

logger = logging.getLogger(__name__)


def get_users(who):
    return User.get_users_from_identifier(who)


# def get_student_users(who):
#     return get_users(who, filter_by_permission_student=True)


def get_team(team_name):
    try:
        return Team.objects.get(name=team_name)
    except Team.DoesNotExist:
        logger.error(f"Failed to get Team with name='{team_name}'")
        raise


def get_team_cards(team, content_item):
    return get_user_cards(team.active_users, content_item)


def get_user_cards(users, content_item):
    cards = set()
    # TODO: ISSUE make this function more efficient
    for user in users:
        for proj in AgileCard.objects.filter(
            content_item=content_item, assignees__in=[user]
        ):
            cards.add(proj)

    return cards


def user_is_competent_for_card_project(card: AgileCard, user: User):
    projects = (
        RecruitProject.objects.filter(content_item=card.content_item)
        .filter(recruit_users__in=[user])
        .filter(complete_time__isnull=False)
    )
    matching_projects = [o for o in projects if o.flavours_match(card.flavour_names)]
    if len(matching_projects) > 0:
        return True
    return False