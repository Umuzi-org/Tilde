from core.models import UserGroup, User, UserGroupMembership
from curriculum_tracking.models import AgileCard


def get_users(who, filter_by_permission_student=False):
    if "@" in who:
        return [User.objects.get(email=who)]
    group = UserGroup.objects.get(name=who)
    memberships = UserGroupMembership.objects.filter(group=group, user__active=True)
    if filter_by_permission_student:
        memberships = memberships.filter(permission_student=True)
    return [o.user for o in memberships]


def get_student_users(who):
    return get_users(who, filter_by_permission_student=True)


def get_group(group_name):
    return UserGroup.objects.get(name=group_name)


def get_group_project_cards(group, content_item):
    return get_user_project_cards(group.active_student_users, content_item)


def get_user_project_cards(users, content_item):
    cards = set()
    # TODO: ISSUE make this function more efficient
    for user in users:
        for proj in AgileCard.objects.filter(
            content_item=content_item, assignees__in=[user]
        ):
            cards.add(proj)

    return cards