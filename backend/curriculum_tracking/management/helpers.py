from core.models import Team, User

from curriculum_tracking.models import AgileCard


def get_users(who):
    if "@" in who:
        return [User.objects.get(email=who)]
    team = Team.objects.get(name=who)
    return team.user_set.filter(active=True)


# def get_student_users(who):
#     return get_users(who, filter_by_permission_student=True)


def get_team(team_name):
    return Team.objects.get(name=team_name)


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